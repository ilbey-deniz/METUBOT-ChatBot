<template>
    <!-- source (only used as template and improved upon): https://www.codeply.com/p/2n5OiAvWd9 -->

    <v-container class="pa-0 fill-height">

        <v-row class="no-gutters elevation-4 fill-height">
            <v-col cols="auto" class="flex-grow-1 flex-shrink-0">
                <v-responsive class="overflow-y-hidden fill-height">
                    <v-card flat class="d-flex flex-column fill-height">
                        <!-- height: 1px deyince tüm problemlerim çözüldü. nasıl bilmiyorum.-->
                        <v-card-text :class="'flex-grow-1 overflow-y-auto ' + scrollbarTheme" ref="message-div"
                                     style="height: 1px;">

                            <template v-for="(msg, i) in messages">
                                <div :class="{ 'd-flex flex-row-reverse': msg.isUser }">
                                  <metubot-chat-message :msg="msg" :enable-did-you-mean-this="enableDidYouMeanThis" @speak="speak(i)"
                                                        :is-speaking="isSpeaking" @select-dymt-question="selectDYMTQuestion"
                                                        @report-question="reportQuestion(i)"></metubot-chat-message>
                                </div>

                            </template>

                            <v-chip v-if="waitingForAnswer"
                                    color="red"
                                    dark
                                    style="height:52px; white-space: normal; width: 70px;"
                                    class="pa-4 mb-2 d-flex justify-center"
                            >
                                <div class="dot-typing"></div>
                            </v-chip>


                        </v-card-text>
                        <v-divider></v-divider>



                        <v-card-text class="flex-shrink-1">
                          <div class="chat-container">
                            <v-text-field
                                    class="center"
                                    v-model="messageForm.content"
                                    label="Bir mesaj yazın"
                                    type="text"
                                    no-details
                                    outlined
                                    @keyup.enter="sendMessage"
                                    hide-details
                            >
                              <template v-slot:prepend>
                                <v-btn class="center" icon @click="toggleRecognition">
                                  <div class="icon-container">
                                    <v-icon
                                        :color="isRecognizing ? 'red' : undefined"
                                        :class="['icons']"
                                    >
                                      {{ isRecognizing ? 'mdi-stop-circle-outline' : 'mdi-microphone' }}</v-icon>
                                  </div>
                                </v-btn>
                              </template>
                              <template v-slot:append-outer>

                                    <!-- touchend.prevent reason is not hiding the keyboard on mobile -->
                                    <v-icon color="blue" @click="sendMessage" @touchend.prevent="sendMessage">
                                        mdi-send
                                    </v-icon>
                                </template>
                            </v-text-field>
                          </div>
                        </v-card-text>
                    </v-card>
                </v-responsive>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import Vue from 'vue'
import {io} from "socket.io-client";
import MetubotChatMessage from '@/components/MetubotChatMessage.vue';
import axios from 'axios';
import * as sdk from 'microsoft-cognitiveservices-speech-sdk';

export default {
    name: 'MetubotChat',
    components: { MetubotChatMessage },
    props: {
        enableDidYouMeanThis: {
            type: Boolean,
            default() {
                return false;
            },
        },
    },
    data() {
        return {
            messages: [],
            messageForm: {
                content: "",
                isUser: true,
                created_at: "11:11am",
                didYouMeanThisQuestions: [],
                selectedDYMTQuestion: null,
            },
            qa_pair: {
                question: "",
                answer: "",
                created_at: "11:11am",
            },
            waitingForAnswer: true,
            socketIoSocket: null,
            reported_question_index: -1,
            answerSoundsEnabled: true,
            text: '',
            voices: [],
            selectedVoice: '',
            transcript: "",
            isRecognizing: false,
            recognition: null,
            isSpeaking: false,
        }
    },
    mounted() {
        this.socketIoSocket = io();
        this.socketIoSocket.on('chat answer',
                msg => setTimeout(() => this.addBotMessage(msg), 777))

        if (this.enableDidYouMeanThis) {
            this.addBotMessage({
                answer: 'Sorunuzu tam anlayamamakla birlikte ileri düzey yöntemlerimiz sayesinde ' +
                        'size şu soruyu yönlendirebiliyoruz:\nŞunlardan birini mi demek istediniz?',
                finished: true,
                didYouMeanThisQuestions: [
                    'Şifremi nasıl şifreleyebilirim?',
                    'Odtüde verilen dersleri öğrenebilir miyim?',
                    'Zart zurt şifremi değiştirmek istiyorum lakin email adresimi sormasına rağmen email adresimin şifresini de bilmiyorum. Ne yapabilirim?',
                ],
                selectedDYMTQuestion: null,
            })
        }
    },
    destroyed() {
        this.socketIoSocket.disconnect();
    },
    methods: {
      // "205d9032223c4a68b5b4f06cce5cc80f", "eastus"
        speak(question_index) {

          if (this.isSpeaking) {
            return; // Return early if already speaking
          }

          this.isSpeaking = true;

          const speechConfig = sdk.SpeechConfig.fromSubscription("205d9032223c4a68b5b4f06cce5cc80f", "eastus");
          speechConfig.speechSynthesisVoiceName = "tr-TR-EmelNeural";

          const speechSynthesizer = new sdk.SpeechSynthesizer(speechConfig);
          const textToSpeak = this.messages[question_index].content;

          speechSynthesizer.speakTextAsync(
              textToSpeak,
              () => {
                // Set isSpeaking to false after speech ends
                speechSynthesizer.close();
              },
              (error) => {
                console.error("Speech synthesis error:", error);
                speechSynthesizer.close();
              }
          );
          setTimeout(() => {
            this.isSpeaking = false; // Delayed execution
          }, 10000); // Replace 10000 with the desired delay in milliseconds
        },
        startRecognition() {
          this.isRecognizing = true;

          const speechConfig = sdk.SpeechConfig.fromSubscription("205d9032223c4a68b5b4f06cce5cc80f", "eastus");
          speechConfig.speechRecognitionLanguage = 'tr-TR';

          const audioConfig = sdk.AudioConfig.fromDefaultMicrophoneInput();
          const recognizer = new sdk.SpeechRecognizer(speechConfig, audioConfig);

          recognizer.recognizing = (s, e) => {
            const result = e.result.text;
            this.transcript = result;
            this.messageForm.content = this.transcript;
            this.sendMessage();
            console.log(result);
          };

          recognizer.canceled = (s, e) => {
            console.error(e.errorDetails);
            this.isRecognizing = false;
          };

          recognizer.sessionStopped = () => {
            console.log('Speech recognition ended');
            this.isRecognizing = false;
          };

          this.recognition = recognizer;
          recognizer.startContinuousRecognitionAsync();
        },
        stopRecognition() {
          this.recognition.stopContinuousRecognitionAsync();
          this.isRecognizing = false;
        },
        toggleRecognition() {
          if (!this.isRecognizing) {
            this.startRecognition();
          } else {
            this.stopRecognition();
          }
        },
        getClock() {
            let date = new Date();
            let hour = date.getHours();
            let minutes = date.getMinutes();
            return `${hour}:${minutes}`;
        },
        selectDYMTQuestion(questionStr) {
            this.messageForm.content = questionStr;
            this.messages[this.messages.length - 1].selectedDYMTQuestion = questionStr;
            this.sendMessage();
        },
        sendMessage() {
            if (this.messageForm.content !== "" && !this.waitingForAnswer) {
                this.messageForm.created_at = this.getClock();
                this.messages.push(this.messageForm);
                this.socketIoSocket.emit('chat question', this.messageForm.content);
                this.messageForm = {
                    content: "",
                    isUser: true,
                    created_at: null,
                    didYouMeanThisQuestions: [],
                    selectedDYMTQuestion: null,
                };
                this.waitingForAnswer = true;
                this.scrollMessagesToBottom();

            }

        },
        addBotMessage(msg) {
            if (msg.finished) {
                this.waitingForAnswer = false;
            }
            if (msg.answer === "") {
                msg.answer = "Sualinize maalesef mütenasip bir yanıt bulamamaktayım. Başka sorunuz varsa lütfen sakınmayınız.";
            }
            this.messages.push({
                content: msg.answer,
                isUser: false,
                created_at: this.getClock(),
                didYouMeanThisQuestions: msg.didYouMeanThisQuestions,
                selectedDYMTQuestion: null,
            });
            this.scrollMessagesToBottom();
            if (this.answerSoundsEnabled) {
                new Audio(require('@/assets/chat-sound-bubble-pop.mp3')).play();
            }
        },
        reportQuestion(question_index) {
            this.speak(question_index);
            // Do not take the first 2 message. Directly ignore them.
            // metubot respond the user message
            // hence, if reported message from metubot and not first 2 message it is an answer to question its above.
            // if reported message from user it is an question the below answer.
            this.reported_question_index = question_index;
            if (question_index > 1 && !this.messages[question_index].isUser) { // it is from metubot
                this.qa_pair.created_at = this.getClock();
                this.qa_pair.answer = this.messages[this.reported_question_index].content;
                if (this.messages[question_index - 1].isUser) {
                    this.qa_pair.question = this.messages[this.reported_question_index - 1].content;
                }
            }
            if (question_index > 1 && this.messages[question_index].isUser) { // it is from user
                this.qa_pair.created_at = this.getClock();
                this.qa_pair.question = this.messages[this.reported_question_index].content;
                if (question_index + 1 < this.messages.length && !this.messages[question_index + 1].isUser) {
                    this.qa_pair.answer = this.messages[this.reported_question_index + 1].content;
                }
            }
            console.log(this.qa_pair.question)
            console.log(this.qa_pair.answer)
            axios.get(`/reportQuestion?question=${this.qa_pair.question}&answer=${this.qa_pair.answer}&created_at=${this.qa_pair.created_at}`)
            this.qa_pair = {
                question: "",
                answer: "",
                created_at: null,
            };
        },

        scrollMessagesToBottom() {
            this.scrollElmToBottomOfElm(this.$refs['message-div']);
        },
        scrollElmToBottomOfElm(element) {
            /* iki next tick gerekti çalışması için. settimeout(, 0) olabilirdi de ama kötü gözüktü */
            Vue.nextTick(() => Vue.nextTick(() => {element.scrollTop = element.scrollHeight;}));
        },
        messagesAtBottom() {
            return this.elmAtBottom(this.$refs['message-div']);
        },
        elmAtBottom(element) {
            return element.scrollHeight - element.scrollTop === element.clientHeight;
        },

    },
    computed: {
        scrollbarTheme() {
            return this.$vuetify.theme.dark ? 'dark-scrollbar' : 'light-scrollbar';
        },
    },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss">
@use 'three-dots' with (
    $dot-width: 8px,
    $dot-height: 8px,
    $dot-color: #ffffff,
);

.fade-enter-active {
    transition: opacity .5s;
}

.fade-leave-active {
    transition: opacity 0s;
}


.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */
{
    opacity: 0;
}

.message-box a {
    color: white !important;
}


.center {
  display: flex;
  align-items: center;
}

.chat-container {
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-container {
  display: flex;
  align-items: center;
  justify-content: center;
}

.icons {
  font-size: 22px;
  width: 30px;
  min-width: 30px;
  text-align: center;
  margin-bottom: 12px;
}


</style>
