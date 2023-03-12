<template>
    <v-hover v-slot:default="{ hover }">
        <v-sheet
                :color="msg.isUser ? 'primary' : 'red'"
                dark
                style="height:auto; position: relative; width: fit-content; border-radius: 19px;"
                class="pa-4 mb-4 message-box"
        >
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



            <v-menu bottom right>
                <template v-slot:activator="{ on, attrs }">
                    <v-btn
                            style="position: absolute; right: 5px; top: 5px;"
                            dark
                            icon
                            v-bind="attrs"
                            v-on="on"
                    >
                        <v-icon v-if="hover">mdi-chevron-down</v-icon>
                    </v-btn>
                </template>

                <v-list>
                    <v-list-item>
                        <v-list-item-title
                                style="cursor:pointer"
                                @click="$emit('report-question')">
                            <span class="material-icons">bug_report</span>
                            <span class="text">Report Question</span>
                        </v-list-item-title>
                    </v-list-item>
                </v-list>
            </v-menu>


        </v-sheet>
    </v-hover>
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


    },
}
</script>

<style scoped>

</style>
