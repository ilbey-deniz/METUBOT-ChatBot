<template>
    <v-container>
        <v-row>
            <v-col>
                <v-card>
                    <v-data-table :headers="headers" :items="qa_pairs" class="elevation-1" :search="search">
                        <template v-slot:top>
                            <v-toolbar flat>
                                <v-toolbar-title>Sorular</v-toolbar-title>
                                <v-divider class="mx-4" inset vertical></v-divider>
                                <v-text-field v-model="search" append-icon="mdi-magnify" label="Arama" single-line
                                    hide-details></v-text-field>
                                <v-spacer></v-spacer>
                                <v-dialog v-model="dialog" max-width="500px">

                                    <template v-slot:activator="{ on, attrs }">
                                        <v-btn color="primary" dark class="mb-2" v-bind="attrs" v-on="on">
                                            Yeni Soru
                                        </v-btn>
                                        <!-- EXCEL INPUTU EKLEME KODU -->
                                        <input type="file" ref="fileInput" @change="selectFile" />
                                        <!-- EXCEL INPUTU EKLEME KODU SONU -->
                                    </template>
                                    <v-card>
                                        <v-card-title>
                                            <span class="text-h5">{{ formTitle }}</span>
                                        </v-card-title>

                                        <v-card-text>
                                            <!--
                                            <v-container>
                                                <v-row>
                                                    <v-col>
                                                        <v-form v-model="valid">
                                                            <v-text-field v-model="editedItem.category" label="Category"
                                                                          prepend-icon="category"
                                                                          :rules="categoryRules" :counter="30"
                                                                          required></v-text-field>
                                                            <v-textarea v-model="editedItem.question" label="Question"
                                                                        prepend-icon="quiz"
                                                                        :rules="questionRules" :counter="200"
                                                                        required></v-textarea>
                                                            <v-textarea v-model="editedItem.answer" label="Answer"
                                                                        prepend-icon="edit_note"
                                                                        :rules="answerRules" :counter="200"
                                                                        required></v-textarea>
                                                            <v-spacer></v-spacer>
                                                        </v-form>
                                                    </v-col>
                                                </v-row>
                                            </v-container>
                                            -->
                                            <v-container>
                                                <v-row>
                                                    <v-col>
                                                        <v-form v-model="valid">
                                                            <v-text-field v-model="editedItem.category" label="Category"
                                                                prepend-icon="category" :rules="categoryRules" :counter="30"
                                                                required></v-text-field>
                                                        </v-form>
                                                    </v-col>

                                                </v-row>
                                                <v-row>
                                                    <v-col>
                                                        <v-form v-model="valid">
                                                            <v-text-field v-model="editedItem.question" label="Question"
                                                                prepend-icon="quiz" :rules="questionRules" :counter="200">
                                                                <template #append>
                                                                    <v-btn class="mb-1" color="gray"
                                                                        @click="addNewQuestion">
                                                                        <v-icon>mdi-plus</v-icon>

                                                                    </v-btn>
                                                                </template>
                                                            </v-text-field>
                                                        </v-form>

                                                    </v-col>
                                                </v-row>
                                                <v-list>
                                                    <template v-for="question in editedItem.questions">
                                                        <v-list-tile :key="index"></v-list-tile>
                                                        <v-list-tile-content>
                                                            <v-list-tile-title>{{ question }}</v-list-tile-title>
                                                        </v-list-tile-content>

                                                        <v-list-tile-action>
                                                            <v-btn icon>
                                                                <v-icon @click.stop="updateItem(index)">
                                                                    add
                                                                </v-icon>
                                                            </v-btn>
                                                        </v-list-tile-action>
                                                    </template>


                                                </v-list>
                                            </v-container>

                                        </v-card-text>

                                        <v-card-actions>
                                            <v-spacer></v-spacer>
                                            <v-btn color="blue darken-1" text @click="close">
                                                İptal
                                            </v-btn>
                                            <v-btn color="blue darken-1" text @click="save">
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
                            <v-icon small class="mr-2" @click="editItem(item)">
                                mdi-pencil
                            </v-icon>
                            <v-icon small @click="deleteItem(item)">
                                mdi-delete
                            </v-icon>
                        </template>
                        <template v-slot:no-data>
                            <v-btn color="primary" @click="initialize">
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

export default {
    name: "AdminQuestionCRUD",
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
            file: '',
            dialog: false,
            dialogDelete: false,
            headers: [
                { text: 'ID', value: 'id'},
                {
                    text: 'Soru',
                    align: 'start',
                    value: 'question',
                },
                { text: 'Cevap', value: 'answer' },
                { text: 'Kategori', value: 'category' },
                { text: 'Actions', value: 'actions', sortable: false },
            ],
            editedIndex: -1,
            editedItem: {
                new_question: '',
                questions: [
                    "question1aaaaaaaaaaaaaaa",
                    "q2",
                    "q3",
                ],
                answer: '',
                category: '',
            },

            defaultItem: {
                new_question: '',
                questions: [],
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

        addNewQuestion() {
            this.editedItem.questions.push(this.editedItem.question)
            this.editedItem.question = ""
        },

        editItem(item) {
            this.editedIndex = this.qa_pairs.indexOf(item)
            this.editedItem = Object.assign({}, item)
            this.dialog = true
        },

        deleteItem(item) {
            this.editedIndex = this.qa_pairs.indexOf(item)
            this.editedItem = Object.assign({}, item)
            this.dialogDelete = true
        },

        deleteItemConfirm() {
            axios.delete(`/deleteQuestion?question_id=${this.editedItem.id}`).then(response => {
                this.qa_pairs.splice(this.editedIndex, 1)
            }).catch(error => {
                console.log(error)
            })
            this.closeDelete()
        },

        //TODO: write close, default is not suitable
        close() {
            this.dialog = false
            this.$nextTick(() => {
                this.editedItem = Object.assign({}, this.defaultItem)
                this.editedIndex = -1
            })
        },

        closeDelete() {
            this.dialogDelete = false
            this.$nextTick(() => {
                this.editedItem = Object.assign({}, this.defaultItem)
                this.editedIndex = -1
            })
        },


        selectFile() {
            const formData = new FormData();
            formData.append('file', this.$refs.fileInput.files[0]);
            console.log(formData)
            axios.post('/upload_excel', formData)
                .then(response => {
                    console.log(response.data);
                })
                .catch(error => {
                    console.log(error);
                });
        },

        save() {
            console.log(this.editedItem)
            if (this.editedIndex > -1) {
                Object.assign(this.qa_pairs[this.editedIndex], this.editedItem);
                if (this.editedItem.question !== "" && this.editedItem.answer !== "" && this.editedItem.category !==
                    "") {
                    this.valid = false;
                } //What does this if do?

                axios.post('/updateQuestion', {id: this.editedItem.id,
                                               question: this.editedItem.question,
                                               answer: this.editedItem.answer,
                                               category: this.editedItem.category}).catch(error => {
                console.log(error);
                })
            }
            else {
                axios.post('/addQuestion', {question: this.editedItem.question,
                                            answer: this.editedItem.answer,
                                            category: this.editedItem.category}).catch(error => {
                console.log(error);
                })
                
                this.qa_pairs.push(this.editedItem);
            }
            this.close()
        },
        submit() {

        },
        initialize() {
            axios.get('/admin/qa_pairs').then(response => {
                this.qa_pairs = response.data;
            }).catch(error => {
                console.log(error)
            })
        },
    },

}
</script>
