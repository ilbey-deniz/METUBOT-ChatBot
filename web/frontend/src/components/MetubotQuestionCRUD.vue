<template>
    <v-container>
        <v-row>
            <v-col>
                <v-card>


                    <v-data-table
                            :headers="headers"
                            :items="qa_pairs"
                            class="elevation-1"
                            :search="search"
                    >
                        <template v-slot:top>
                            <v-toolbar
                                    flat
                            >
                                <v-toolbar-title>Sorular</v-toolbar-title>
                                <v-divider
                                        class="mx-4"
                                        inset
                                        vertical
                                ></v-divider>
                                <v-text-field
                                        v-model="search"
                                        append-icon="mdi-magnify"
                                        label="Arama"
                                        single-line
                                        hide-details
                                ></v-text-field>
                                <v-spacer></v-spacer>
                                <v-dialog
                                        v-model="dialog"
                                        max-width="500px"
                                >
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-btn
                                                color="primary"
                                                dark
                                                class="mb-2"
                                                v-bind="attrs"
                                                v-on="on"
                                        >
                                            Yeni Soru
                                        </v-btn>
                                    </template>
                                    <v-card>
                                        <v-card-title>
                                            <span class="text-h5">{{ formTitle }}</span>
                                        </v-card-title>

                                        <v-card-text>
                                            <v-container>
                                                <v-row>
                                                    <v-col>
                                                        <v-form  v-model="valid">
                                                            <v-text-field v-model="editedItem.category" label="Category"
                                                                          prepend-icon="category"
                                                                          :rules="categoryRules" :counter="30"
                                                                          required></v-text-field>
                                                            <v-textarea v-model="editedItem.question" label="Question"
                                                                        prepend-icon="quiz"
                                                                        :rules="questionRules" :counter="200"
                                                                        required></v-textarea>
                                                            <!-- question_mark may also be used -->
                                                            <v-textarea v-model="editedItem.answer" label="Answer"
                                                                        prepend-icon="edit_note"
                                                                        :rules="answerRules" :counter="200"
                                                                        required></v-textarea>
                                                            <v-spacer></v-spacer>
                                                        </v-form>
                                                    </v-col>
                                                </v-row>
                                            </v-container>
                                        </v-card-text>

                                        <v-card-actions>
                                            <v-spacer></v-spacer>
                                            <v-btn
                                                    color="blue darken-1"
                                                    text
                                                    @click="close"
                                            >
                                                İptal
                                            </v-btn>
                                            <v-btn
                                                    color="blue darken-1"
                                                    text
                                                    @click="save"
                                            >
                                                Tamam
                                            </v-btn>
                                        </v-card-actions>
                                    </v-card>
                                </v-dialog>
                                <v-dialog v-model="dialogDelete" max-width="500px">
                                    <v-card>
                                        <v-card-title class="text-h5">Silmek istediğinize emin misiniz?
                                        </v-card-title>
                                        <v-card-actions>
                                            <v-spacer></v-spacer>
                                            <v-btn color="blue darken-1" text @click="closeDelete">İptal</v-btn>
                                            <v-btn color="blue darken-1" text @click="deleteItemConfirm">Evet</v-btn>
                                            <v-spacer></v-spacer>
                                        </v-card-actions>
                                    </v-card>
                                </v-dialog>
                            </v-toolbar>
                        </template>
                        <template v-slot:item.actions="{ item }">
                            <v-icon
                                    small
                                    class="mr-2"
                                    @click="editItem(item)"
                            >
                                mdi-pencil
                            </v-icon>
                            <v-icon
                                    small
                                    @click="deleteItem(item)"
                            >
                                mdi-delete
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
                    </v-data-table>
                </v-card>

            </v-col>
        </v-row>


    </v-container>

</template>

<script>
import axios from 'axios'
// import Vue from 'vue'
import { io } from "socket.io-client";
import AdminView from '../views/AdminView.vue'

export default {
    name: "MetubotQuestionCRUD",
    components: {
        AdminView,
    },
    data() {
        return {
            valid: false,

            categoryRules: [
                v => !!v || 'category is required',
                v => v.length <= 30 || 'category must be less than 30 characters',
            ],

            questionRules: [
                v => !!v || 'question is required',
            ],

            answerRules: [
                v => !!v || 'answer is required',
            ],
            socketIoSocket: null,
            search: '',

            qa_pairs: [],

            dialog: false,
            dialogDelete: false,
            headers: [
                {
                    text: 'Soru',
                    align: 'start',
                    value: 'question',
                },
                { text: 'Cevab', value: 'answer' },
                { text: 'Kategori', value: 'category' },
                { text: 'Actions', value: 'actions', sortable: false },
            ],
            editedIndex: -1,
            editedItem: {
                question: '',
                answer: '',
                category: '',
            },

            defaultItem: {
                question: '',
                answer: '',
                category: '',
            },

        }
    },
    mounted() {
        this.socketIoSocket = io();
        this.initialize();
    },
    computed: {
        formTitle() {
            return this.editedIndex === -1 ? 'Yeni Soru' : 'Soru Düzenle'
        },
    },
    watch: {
        dialog(val) {
            val || this.close()
        },
        dialogDelete(val) {
            val || this.closeDelete()
        },
    },

    methods: {

        editItem (item) {
            this.editedIndex = this.qa_pairs.indexOf(item)
            this.editedItem = Object.assign({}, item)
            this.dialog = true
        },

        deleteItem (item) {
            this.editedIndex = this.qa_pairs.indexOf(item)
            this.editedItem = Object.assign({}, item)
            this.dialogDelete = true
        },

        deleteItemConfirm () {
            this.qa_pairs.splice(this.editedIndex, 1)
            this.closeDelete()
        },

        close () {
            this.dialog = false
            this.$nextTick(() => {
                this.editedItem = Object.assign({}, this.defaultItem)
                this.editedIndex = -1
            })
        },

        closeDelete () {
            this.dialogDelete = false
            this.$nextTick(() => {
                this.editedItem = Object.assign({}, this.defaultItem)
                this.editedIndex = -1
            })
        },

        save () {
            console.log(this.editedItem)
            if (this.editedIndex > -1) {
                Object.assign(this.qa_pairs[this.editedIndex], this.editedItem);
                if (this.category !== "" && this.answer !== "" && this.question !== "") {
                    this.socketIoSocket.emit('add question', this.editedItem);
                    this.valid = false;
                }
            } else {
                this.qa_pairs.push(this.editedItem);
            }
            this.close()
        },
        submit() {

        },
        initialize() {
            axios.get('/admin/qa_pairs').then(response => {
                this.qa_pairs = response.data['qa-pairs'];
            }).catch(error => {
                console.log(error)
            })
        }
    },


}
</script>
