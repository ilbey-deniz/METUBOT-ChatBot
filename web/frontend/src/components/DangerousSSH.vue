<template>
    <!-- source (only used as template and improved upon): https://www.codeply.com/p/2n5OiAvWd9 -->

    <v-container class="pa-0 fill-height">
        <v-row class="no-gutters elevation-4 fill-height">
            <v-col cols="auto" class="flex-grow-1 flex-shrink-0">
                <v-responsive class="overflow-y-hidden fill-height">
                    <v-card flat class="d-flex flex-column fill-height">
                        <v-card-text :class="'flex-grow-1 overflow-y-auto ' + scrollbarTheme">
                            <div class="ssh-out"
                                 style="height: calc(100vh - 200px); overflow: auto;">
                                <p v-for="out in orderedSshOuts" class="py-0 my-0" style="white-space:pre;">{{ out.content }}</p>


                            </div>


                        </v-card-text>
                        <v-divider></v-divider>
                        <v-card-text class="flex-shrink-1">
                            <v-text-field
                                    v-model="sshInForm.content"
                                    label="Komut"
                                    type="text"
                                    no-details
                                    outlined
                                    @keyup.enter="sendMessage"
                                    prepend-inner-icon="mdi-greater-than"
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
    name: 'DangerousSSH',
    props: {},
    data() {
        return {
            sshOuts: [],
            sshInForm: {
                content: "",
            },

            socketIoSocket: null,

        }
    },
    mounted() {
        this.socketIoSocket = io();
        this.socketIoSocket.on('ssh out', (msg) => {
            this.sshOuts.push(msg);
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
            if (this.sshInForm.content !== "") {
                this.socketIoSocket.emit('ssh in', this.sshInForm.content);
                this.sshInForm = {
                    content: "",

                };

            }

        },

    },
    computed: {
        scrollbarTheme() {
            return this.$vuetify.theme.dark ? 'dark-scrollbar' : 'light-scrollbar';
        },
        orderedSshOuts() {
            return this.sshOuts.sort((a, b) => a.sshSeqNum - b.sshSeqNum);
        },
    },

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
@use 'three-dots' with (
    $dot-width: 8px,
    $dot-height: 8px,
    $dot-color: gray,
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

.ssh-out * {
    font-family: Consolas, monaco, monospace;
}

</style>
