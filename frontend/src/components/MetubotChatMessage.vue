<template>
    <div>

        <v-menu offset-y v-model="feedbackMenu">
            <template v-slot:activator="{ on }">
                <v-hover v-slot:default="{ hover }">
                    <v-sheet
                            :color="msg.isUser ? 'primary' : 'red'"
                            dark
                            style="height:auto; position: relative; width: fit-content; border-radius: 19px;"
                            class="pa-4 mb-4 message-box"
                            
                    >
                        <v-btn @click="feedbackMenu = true" style="position: absolute; right: 5px; top: 5px;" dark icon>

                            <v-icon v-if="hover">mdi-chevron-down</v-icon>

                        </v-btn> 
                        
                        <span v-if="typeof msg.content === 'string'" v-html="sanitizeExceptBoldItalicCode(msg.content).trim()" v-linkified
                              style="white-space: pre-wrap;"> </span>
     
                        <span v-else>
                            {{ msg.content.answer[Math.floor(Math.random()*msg.content.answer.length)] }}
                        </span>

                        <span v-if="msg.content.buttons">
                          <v-alert
                              v-for="button in msg.content.buttons"
                              color="indigo"
                              icon="mdi-send"
                              border="left"
                              @click="$emit('select-button', button)"
                              dense
                              style="cursor: pointer; font-size:0.875rem; width:fit-content"
                              class="mt-3"
                          >
                          
                          {{ button.text }}
                          </v-alert>
                        </span> 
                        <span v-if="enableDidYouMeanThis && !msg.selectedDYMTQuestion">
                        <v-alert
                                v-for="question in msg.didYouMeanThisQuestions"
                                color="indigo"
                                icon="mdi-send"
                                border="left"
                                @click="$emit('select-dymt-question',question)"
                                dense
                                style="cursor: pointer; font-size:0.875rem; width:fit-content"
                                class="mt-3"
                        >
                        {{ question }}
                        </v-alert>

                    </span>
                        <sub class="ml-2"
                             style="font-size: 0.6rem; display: block; text-align: right; color: #ddd">{{
                                addPadding(msg.created_at)
                            }}
                        </sub>
                    </v-sheet>
                </v-hover>
            </template>
            <v-list dense flat>
                <v-list-item @click="onLike" v-if="!feedback || feedback === 'like'">
                    <v-list-item-icon>
                        <v-icon :color="feedback ? 'green' : ''">mdi-thumb-up</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                        <v-list-item-title v-if="feedback">Beğenildi</v-list-item-title>
                        <v-list-item-title v-else>Beğen</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item @click="onDislike" v-if="!feedback || feedback === 'dislike'">
                    <v-list-item-icon>
                        <v-icon :color="feedback ? 'red' : ''">mdi-thumb-down</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                        <v-list-item-title v-if="feedback">Beğenilmedi</v-list-item-title>
                        <v-list-item-title v-else @click="onDislike">Beğenme</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item @click="onFeedback">
                    <v-list-item-icon>
                        <v-icon>mdi-bug</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                        <v-list-item-title>Fazladan geri bildirim</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </v-list>

        </v-menu>
        <v-dialog
                v-model="feedbackDialog"
                max-width="600"
        >
            <v-card>
                <v-card-title class="text-h5">
                    Geri bildirim gönder
                </v-card-title>
                <v-card-text>
                    <v-textarea
                            class="mt-4"
                            solo
                            label="Cevap hakkında ne düşünüyorsunuz?"
                            v-model="feedbackText"
                    ></v-textarea>
                </v-card-text>


                <v-card-actions>
                    <v-spacer></v-spacer>

                    <v-btn
                            color="gray darken-1"
                            text
                            @click="resetFeedbackDialog"
                    >
                        İptal
                    </v-btn>

                    <v-btn
                            color="green darken-1"
                            text
                            @click="sendFeedbackText"
                    >
                        Geri bildirimi gönder
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>


</template>

<script>
import axios from "axios";

export default {
    name: "MetubotChatMessage",
    props: {
        msg: Object,
        enableDidYouMeanThis: {
            type: Boolean,
            default() {
                return false;
            },
        },
    },
    data() {
        return {
            feedbackMenu: false,
            feedback: '',
            feedbackText: '',
            feedbackDialog: false,
        }
    },
    methods: {
        sanitizeExceptBoldItalicCode(str) {
            return this.$sanitize(str);
        },
        addPadding(hourAndMinuteStr) {
            let hourAndMinute = hourAndMinuteStr.split(":");
            let hour = hourAndMinute[0];
            let minute = hourAndMinute[1];
            if (hour.length === 1) {
                hour = "0" + hour;
            }
            if (minute.length === 1) {
                minute = "0" + minute;
            }
            return hour + ":" + minute;
        },
        addFeedbackRequest(asked_question_id, feedback='', feedbackText='') {
            axios.get(`/addFeedback?asked_question_id=${asked_question_id}&report_message=${feedbackText}&is_liked=${feedback}`)
                .then(response => {
                    console.log(response);
                })
                .catch(error => {
                    console.log(error);
                });
        },
        onLike() {
            if (this.feedback !== 'like') {
                this.feedback = 'like';
                this.feedbackText = '';
                this.addFeedbackRequest(this.msg.asked_question_id, this.feedback, this.feedbackText);
                this.feedbackDialog = true;
            }

        },
        onDislike() {
            if (this.feedback !== 'dislike') {
                this.feedback = 'dislike';
                this.feedbackText = '';
                this.addFeedbackRequest(this.msg.asked_question_id, this.feedback, this.feedbackText);
                this.feedbackDialog = true;
            }
        },
        onFeedback() {
            this.feedbackDialog = true;
        },
        resetFeedbackDialog() {
            this.feedbackText = '';
            this.feedbackDialog = false;
        },
        sendFeedbackText() {
            this.addFeedbackRequest(this.msg.asked_question_id, '', this.feedbackText);
            this.resetFeedbackDialog();
        }

    },
}
</script>

<style scoped>

</style>
