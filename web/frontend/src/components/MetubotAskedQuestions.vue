<!-- <template>
    
    <div>
        <v-container class="pa-0 fill-height">
            <v-row>
                <v-col>
                    <admin-view class="mt-5"/>
                </v-col>
            </v-row>

        </v-container>

    </div>
</template> -->
<template>
    <!-- <AdminView /> -->
    <div class="main">
        <v-card class="card">
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
    </div>
    
</template>

<script>
import AdminView from '../views/AdminView.vue'

export default {
    name: "MetubotAskedQuestions",
    components: {
        AdminView,
    },
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
    .main {
        /* justify-content: center; */
        padding-left: 3%;   
        padding-top: 3%;   
        padding-right: 3%;
        height: fit-content;
        width: 100%;   
    }
    /* .card {
        margin-left: 3%;
        margin-right: 3%; 
        margin-top: 3%;
         margin: 3% 3% 3% 3%;
        height: fit-content;
        width: 94%;
        
    } */
</style>
