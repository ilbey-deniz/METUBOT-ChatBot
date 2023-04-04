<template class="main">
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
</template>

<script>
import QAPairs from '../../../Elasticsearch/qa_pairs.json'

export default {
    name: "AdminDashboard",
    data() {
        return {
            search: '',
            questions: [ // temporary. the real questions will be requested from the database.
                QAPairs
            ],
            headers: [
                {
                    text: 'Soru',
                    align: 'start',
                    sortable: true,
                    value: 'question',
                },
                { text: 'Cevap', value: 'category' },
                { text: 'Kategori', value: 'category' },
            ],
        }
    },
}
</script>

<style scoped>
    /* .main {
        justify-content: center;
    } */
    .card {
        margin-left: 3%;
        margin-right: 3%;
        margin-top: 3%;
        height: fit-content;
        width: 100%;
    }
</style>
