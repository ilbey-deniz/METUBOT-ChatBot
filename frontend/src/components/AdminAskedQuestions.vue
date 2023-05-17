<template>
    <div class="main">
        <v-card>
            <v-card-text style="height: 400px;" class="d-flex align-center justify-center">
                <admin-chart-pie :data="chartData"/>
            </v-card-text>

        </v-card>
        <v-card class="card mt-4">
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
                    :items-per-page="50"
                    :items-per-page-text="'hl'"
                    no-results-text="Sonuç bulunamadı."
                    no-data-text="Soru bulunmamaktadır."
                    :footer-props="{'items-per-page-text':'Sayfa başı gösterilecek soru sayısı:'}"
            >

                <template v-slot:item.feedback="{ item }">
                    <v-icon
                            v-if="item.feedback === 'like'"
                            small
                            class="mr-2"
                            @click="editItem(item)"
                    >
                        mdi-thumb-up
                    </v-icon>
                    <v-icon
                            v-if="item.feedback === 'dislike'"
                            small
                            @click="deleteItem(item)"
                    >
                        mdi-thumb-down
                    </v-icon>
                    <v-icon
                            v-if="item.feedback === ''"
                            small
                            @click="deleteItem(item)"
                    >
                        mdi-tilde
                    </v-icon>

                </template>
                <template v-slot:no-data>
                    <v-btn
                            color="primary"
                            @click="initialize"
                    >
                        Reset
                    </v-btn>
                </template>
                <template v-slot:[`footer.page-text`]="items">
                    {{ items.pageStart }} - {{ items.pageStop }} / {{ items.itemsLength }}
                </template>

            </v-data-table>
        </v-card>

    </div>

</template>

<script>
import AdminChartPie from '@/components/AdminChartPie.vue';
import axios from 'axios';

export default {
    name: "AdminAskedQuestions",
    components: { AdminChartPie },
    data() {
        return {
            search: '',
            questions: [ // temporary. the real questions will be requested from the database.
                /*{
                    question: "Bugün ne yiyeceğiz?",
                    matchedQuestion: "Bugün pilav üstü odtü kavurma yiyeceğiz.",
                    category: "kafeterya",
                    similarity: 0.8,
                    feedback: 'like',
                    feedbackText: 'Ben bu cevabı ziyadesiyle beğendim, filhakika bu hoş feedbacki bile bırakmış bulundum.',
                }*/
            ],
            headers: [
                {
                    text: 'Sorulan Soru',
                    align: 'start',
                    value: 'question',
                },
                { text: 'Eşleşen Soru', value: 'matchedQuestion' },
                { text: 'Kategori', value: 'category' },
                { text: 'Benzerlik', value: 'similarity' },
                { text: 'Beğeni', value: 'feedback' },
                { text: 'Geri Bildirim', value: 'feedbackText' },
                { text: 'Tarih', value: 'created_at' },
            ],
        }
    },
    mounted() {
        axios.get('/askedQuestions')
            .then(response => {
                this.questions = response.data.data;
            })
            .catch(error => {
                console.log(error);
            });
    },
    computed: {
        chartData() {
            const catToCount = {};
            this.questions.forEach((question) => {
                if (catToCount[question.category]) {
                    catToCount[question.category] += 1;
                }
                else {
                    catToCount[question.category] = 1;
                }
            });
            const data = {
                labels: Object.keys(catToCount),
                datasets: [
                    {
                        label: 'Sorulan Sorular',
                        data: Object.values(catToCount),
                        backgroundColor: this.getNRandomColors(Object.keys(catToCount).length),
                        hoverOffset: 4,
                    },
                ],
            };
            return data;

        },
    },
    methods: {
        getNRandomColors(n) {
            const colors = [];
            for (let i = 0; i < n; i++) {
                colors.push(`rgb(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)})`);
            }
            return colors;
        },
    }
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
