<template>
    <div>
        <v-container class="pa-0 fill-height">
            <v-row>
                <v-col>
                    <metubot-asked-questions class="mt-5"/>
                </v-col>
            </v-row>

        </v-container>

    </div>
</template>

<script>
import MetubotAskedQuestions from '@/components/MetubotAskedQuestions.vue'

export default {
    name: 'AdminView',
    components: {
        MetubotAskedQuestions,
    },
}

</script>
