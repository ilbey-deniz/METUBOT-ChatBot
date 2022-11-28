<template>
    <!-- source: https://www.codeply.com/p/2n5OiAvWd9 -->
    <v-container class="pa-0 fill-height">
        <v-row class="no-gutters elevation-4">
            <v-col cols="auto" class="flex-grow-1 flex-shrink-0">
                <v-responsive class="overflow-y-hidden">
                    <v-card flat class="d-flex flex-column asdf" :style="{height: `calc(100vh - ${appBarHeight}px)` }">


                        <v-card-text :class="'flex-grow-1 overflow-y-auto ' + scrollbarTheme">
                            <template v-for="(msg, i) in messages">
                                <div :class="{ 'd-flex flex-row-reverse': msg.me }">
                                    <v-menu offset-y>
                                        <template v-slot:activator="{ on }">
                                            <v-hover v-slot:default="{ hover }">
                                                <v-chip
                                                        :color="msg.me ? 'primary' : 'red'"
                                                        dark
                                                        style="height:auto;white-space: normal;"
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
                        </v-card-text>
                        <v-divider></v-divider>
                        <v-card-text class="flex-shrink-1">
                            <v-text-field
                                    v-model="messageForm.content"
                                    label="Mesaj"
                                    type="text"
                                    no-details
                                    outlined
                                    append-outer-icon="mdi-send"
                                    @keyup.enter="messages.push(messageForm)"
                                    @click:append-outer="messages.push(messageForm)"
                                    hide-details
                            />

                        </v-card-text>

                    </v-card>
                </v-responsive>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import axios from 'axios'

export default {
    name: 'MetubotChat',
    props: {
        appBarHeight: Number,
    },
    data() {
        return {

            messages: [
                {
                    content: "Merhaba, ben Metubot 🤖",
                    me: false,
                    created_at: "11:11",
                },
                {
                    content: "Sizlere nasıl yardımcı olabilirim?",
                    me: false,
                    created_at: "11:11",
                },
            ],
            messageForm: {
                content: "",
                me: true,
                created_at: "11:11am",
            },
        }
    },
    methods: {
        sendMessageToServer() {
            axios.post(`/`, {
                question: this.chatMessage,
            });
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
<style scoped>


</style>
