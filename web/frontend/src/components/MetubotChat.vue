<template>
    <!-- source (only used as template and improved upon): https://www.codeply.com/p/2n5OiAvWd9 -->

    <v-container class="pa-0 fill-height">

        <v-row class="no-gutters elevation-4 fill-height">
            <v-col cols="auto" class="flex-grow-1 flex-shrink-0">
                <v-responsive class="overflow-y-hidden fill-height">
                    <v-card flat class="d-flex flex-column fill-height">


                        <v-card-text :class="'flex-grow-1 overflow-y-auto ' + scrollbarTheme">
                            <template v-for="(msg, i) in messages">
                                <div :class="{ 'd-flex flex-row-reverse': msg.isUser }">
                                    <v-menu offset-y>
                                        <template v-slot:activator="{ on }">
                                            <v-hover v-slot:default="{ hover }">
                                                <v-chip
                                                        :color="msg.isUser ? 'primary' : 'red'"
                                                        dark
                                                        style="height:auto;white-space: normal; white-space: pre-wrap;"
                                                        class="pa-4 mb-2"
                                                        v-on="on"
                                                >
                                                    {{ msg.content }}
                                                    <sub class="ml-2" style="font-size: 0.5rem;">
                                                        {{ msg.created_at }}
                                                    </sub>
                                                    <v-icon v-if="hover" small>mdi-chevron-down</v-icon>
                                                </v-chip>
                                            </v-hover>
                                        </template>
                                        <v-list>
                                            <v-list-item>
                                                <v-list-item-title>delete</v-list-item-title>
                                            </v-list-item>
                                        </v-list>
                                    </v-menu>
                                </div>
                            </template>
                            <transition name="fade">
                                <v-chip v-if="waitingForAnswer"
                                        color="red"
                                        dark
                                        style="height:auto; white-space: normal; width: 70px;"
                                        class="pa-4 mb-2 d-flex justify-center"
                                >
                                    <div class="dot-typing"></div>
                                    <!--                                <div class="dot-typing"></div>
                                                                    <div class="dot-elastic"></div>-->
                                </v-chip>
                            </transition>

                        </v-card-text>
                        <v-divider></v-divider>
                        <v-card-text class="flex-shrink-1">
                            <v-text-field
                                    v-model="messageForm.content"
                                    label="Mesaj"
                                    type="text"
                                    no-details
                                    outlined
                                    @keyup.enter="sendMessage"
                                    hide-details
                            >
                                <template v-slot:append-outer>
                                    <!-- touchend.prevent reason is not hiding the keyboard on mobile -->
                                    <v-icon @click="sendMessage" @touchend.prevent="sendMessage">
                                        mdi-send
                                    </v-icon>

                                </template>
                            </v-text-field>
                        </v-card-text>
                    </v-card>
                </v-responsive>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import axios from 'axios'
import Vue from 'vue'
import { io } from "socket.io-client";

export default {
    name: 'MetubotChat',
    props: {},
    data() {
        return {
            messages: [
                /*{
                    content: "Merhaba, ben Metubot 🤖",
                    isUser: false,
                    created_at: this.getClock(),
                },*/
            ],
            messageForm: {
                content: "",
                isUser: true,
                created_at: "11:11am",
            },
            waitingForAnswer: true,
            socketIoSocket: null,
        }
    },
    mounted() {
        this.socketIoSocket = io();
        this.socketIoSocket.on('chat answer', (msg) => {
            this.waitingForAnswer = false;
            if (msg === "") {
                msg = "Sualinize maalesef mütenasip bir yanıt bulamamaktayım. Başka sorunuz varsa lütfen sakınmayınız.";
            }
            this.messages.push({
                content: msg,
                isUser: false,
                created_at: this.getClock(),
            });
        })
    },
    methods: {
        sendMessageToServer() {
            axios.post(`/`, {
                question: this.chatMessage,
            });
        },
        getClock() {
            let date = new Date();
            let hour = date.getHours();
            let minutes = date.getMinutes();
            return `${hour}:${minutes}`;
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
                };
                this.waitingForAnswer = true;

            }

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
<style scoped lang="scss">
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

</style>
