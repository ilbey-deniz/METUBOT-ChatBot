<template>
    <v-menu offset-y>
        <template v-slot:activator="{ on, attrs }">
            <v-hover v-slot:default="{ hover }">
                <v-sheet
                        :color="msg.isUser ? 'primary' : 'red'"
                        dark
                        style="height:auto; position: relative; width: fit-content; border-radius: 19px;"
                        class="pa-4 mb-4 message-box"
                        v-bind="attrs"
                        v-on="on"
                >
                    <v-btn
                            style="position: absolute; right: 5px; top: 5px;"
                            dark
                            icon

                    >
                        <v-icon v-if="hover">mdi-chevron-down</v-icon>
                    </v-btn>
                    <span v-html="sanitizeExceptBoldItalicCode(msg.content).trim()" v-linkified
                          style="white-space: pre-wrap;"/>
                    <span v-if="enableDidYouMeanThis">
                  <template v-if="!msg.selectedDYMTQuestion">
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
                  </template>
               </span>
                    <sub class="ml-2"
                         style="font-size: 0.6rem; display: block; text-align: right; color: #ddd">{{
                            addPadding(msg.created_at)
                        }}</sub>

                </v-sheet>
            </v-hover>
        </template>
        <v-list dense flat>
            <v-list-item-group>
                <v-list-item v-if="!feedback || feedback === 'like'">
                    <v-list-item-icon>
                        <v-icon :color="feedback ? 'green' : ''">mdi-thumb-up</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                        <v-list-item-title v-if="feedback" @click="onLike">Beğenildi</v-list-item-title>
                        <v-list-item-title v-else @click="onLike">Beğen</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item v-if="!feedback || feedback === 'dislike'">
                    <v-list-item-icon>
                        <v-icon :color="feedback ? 'red' : ''">mdi-thumb-down</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                        <v-list-item-title v-if="feedback" @click="onDislike">Beğenilmedi</v-list-item-title>
                        <v-list-item-title v-else @click="onDislike">Beğenme</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item>
                    <v-list-item-icon>
                        <v-icon>mdi-bug</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                        <v-list-item-title @click="$emit('report-question')">Hata raporla</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </v-list-item-group>

        </v-list>

    </v-menu>
</template>

<script>
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
            feedback: '',
            feedbackText: '',
            likeDialog: false,
            dislikeDialog: false,
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
        onLike() {
            this.feedback = 'like';
            this.likeDialog = true;


        },
        onDislike() {
            this.feedback = 'dislike';
            this.dislikeDialog = true;
        }

    },
}
</script>

<style scoped>

</style>
