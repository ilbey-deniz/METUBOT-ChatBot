<template>
    <v-card >
        <v-card-title>
            Sorulan Sorular
            <v-spacer></v-spacer>
            <v-text-field
                    v-model="search"
                    append-icon="mdi-magnify"
                    label="Arama"

            ></v-text-field>
        </v-card-title>

        <v-data-table
                :headers="headers"
                :items="questions"
                :search="search"
                :items-per-page="5"
                :items-per-page-text="'hl'"
                no-results-text="Sonuç bulunamadı."
                no-data-text="Soru bulunmamaktadır."
                :footer-props="{
                'items-per-page-text':'Sayfa başı gösterilecek soru sayısı:',
              }"
        >


            <template v-slot:[`footer.page-text`]="items">
                {{ items.pageStart }} - {{ items.pageStop }} / {{ items.itemsLength }}
            </template>
        </v-data-table>
    </v-card>

</template>

<script>
export default {
    name: "MetubotAskedQuestions",
    data() {
        return {
            search: '',
            questions: [ // temporary. the real questions will be requested from the database.
                {
                    question: "Bugün ne yiyeceğiz?",
                    matchedQuestion: "Bugün pilav üstü odtü kavurma yiyeceğiz.",
                    similarity: 0.8,

                },
                {
                    question: "Şifremi nasıl öğrenebilirim?",
                    matchedQuestion: "Şifrenizi öğrenmek için şifre sıfırlama sayfasına gidiniz.",
                    similarity: 0.6,
                },
                {
                    question: "Bugün ne yiyeceğiz?",
                    matchedQuestion: "Bugün pilav üstü odtü kavurma yiyeceğiz.",
                    similarity: 0.8,

                },
                {
                    question: "Şifremi nasıl öğrenebilirim?",
                    matchedQuestion: "Şifrenizi öğrenmek için şifre sıfırlama sayfasına gidiniz.",
                    similarity: 0.6,
                },
                {
                    question: "Bugün ne yiyeceğiz?",
                    matchedQuestion: "Bugün pilav üstü odtü kavurma yiyeceğiz.",
                    similarity: 0.8,

                },
                {
                    question: "Şifremi nasıl öğrenebilirim?",
                    matchedQuestion: "Şifrenizi öğrenmek için şifre sıfırlama sayfasına gidiniz.",
                    similarity: 0.6,
                },
                {
                    question: "Bugün ne yiyeceğiz?",
                    matchedQuestion: "Bugün pilav üstü odtü kavurma yiyeceğiz.",
                    similarity: 0.8,

                },
                {
                    question: "Şifremi nasıl öğrenebilirim?",
                    matchedQuestion: "Şifrenizi öğrenmek için şifre sıfırlama sayfasına gidiniz.",
                    similarity: 0.6,
                },
            ],
            headers: [
                {
                    text: 'Sorulan Soru',
                    align: 'start',
                    sortable: true,
                    value: 'question',
                },
                { text: 'Eşleşen Soru', value: 'matchedQuestion' },
                { text: 'Benzerlik', value: 'similarity' },
            ],
        }
    },
}
</script>

<style scoped>

</style>
