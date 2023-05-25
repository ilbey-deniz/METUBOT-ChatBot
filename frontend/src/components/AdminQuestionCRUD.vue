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
                                <v-dialog v-model="dialog" max-width="800px" scrollable >

                                    <template v-slot:activator="{ on, attrs }">
                                        <v-btn color="primary" dark class="mb-2" v-bind="attrs" v-on="on">
                                            Yeni Soru
                                        </v-btn>
                                        <!-- EXCEL INPUTU EKLEME KODU -->
                                        <input type="file" ref="fileInput" @change="selectFile" />
                                        <!-- EXCEL INPUTU EKLEME KODU SONU -->
                                    </template>
                                    <v-card>
                                        <v-card-title class="pa-0 ma-0">
                                            <v-toolbar flat>
                                                <v-toolbar-title>{{ formTitle }}</v-toolbar-title>
                                            </v-toolbar>
                                        </v-card-title>

                                        <v-divider></v-divider>

                                        <v-card-text>
                                            <v-container>
                                                <v-card flat class="ma-1" outlined>
                                                    <v-col class="pa-0 ma-0">
                                                        <v-form v-model="valid" class="pa-2">
                                                            <v-text-field v-model="editedItem.category" label="Category"
                                                                prepend-icon="category" :rules="categoryRules" :counter="30"
                                                                required></v-text-field>
                                                        </v-form>
                                                    </v-col>
                                                </v-card>

                                                <v-card flat class="ma-1" outlined>
                                                    <v-col class="pa-0 ma-0">
                                                        <v-form v-model="valid" class="pa-2">
                                                            <v-text-field v-model="editedItem.new_question" label="Question"
                                                                prepend-icon="quiz" :counter="200">
                                                                <template #append>
                                                                    <v-btn icon class="mb-1" color="gray"
                                                                        @click="addNewQuestion" :disabled="editedItem.new_question.length == 0">
                                                                        <v-icon>mdi-plus</v-icon>
                                                                    </v-btn>
                                                                </template>
                                                            </v-text-field>
                                                        </v-form>

                                                        <v-divider></v-divider>
                                                        
                                                        <v-layout row class="pa-2">
                                                            <v-container style="height: 200px;" class="pa-2 ma-2 overflow-y-auto">
                                                                <v-row 
                                                                    v-for="(question, index) in editedItem.questions" 
                                                                    class="pa-0 ma-0"
                                                                >
                                                                    <v-row class="pa-0 ma-0" v-if="editedQuestionIndex == index">
                                                                        <v-col cols="11">
                                                                            <v-text-field 
                                                                                v-model="editedItem.questions[index]"
                                                                                underlined
                                                                                flat
                                                                                dense
                                                                                height="20px"
                                                                                hide-details="auto"
                                                                            >
                                                                            </v-text-field>
                                                                        </v-col>
                                                                        <v-col class="text-right" cols="1">
                                                                            <v-icon @click.stop="saveQuestion(index)">
                                                                                done
                                                                            </v-icon>
                                                                        </v-col>
                                                                    </v-row>

                                                                    <v-row class="pa-0 ma-0" v-else style="width: 100%;">
                                                                        <v-col v-text="question" cols="10"></v-col>
                                                                        <v-col class="text-right" cols="1">
                                                                            <v-icon @click.stop="updateQuestion(index)">
                                                                                edit
                                                                            </v-icon>
                                                                        </v-col>
                                                                        <v-col class="text-right" cols="1">
                                                                            <v-icon @click.stop="deleteQuestion(index)" :disabled="editedQuestionIndex != -1">
                                                                                delete
                                                                            </v-icon>
                                                                        </v-col>
                                                                    </v-row>
                                                                
                                                                </v-row>
                                                            </v-container>
                                                        </v-layout>
                                                    </v-col>
                                                </v-card>

                                                
                                                <v-card flat class="ma-1" outlined>
                                                    <v-col class="pa-0 ma-0">
                                                        <v-form v-model="valid" class="pa-2">
                                                            <v-text-field v-model="editedItem.new_answer" label="Answer"
                                                                prepend-icon="question_answer" :counter="200">
                                                                <template #append>
                                                                    <v-btn icon class="mb-1" color="gray"
                                                                        @click="addNewAnswer" :disabled="editedItem.new_answer.length == 0">
                                                                        <v-icon>mdi-plus</v-icon>
                                                                    </v-btn>
                                                                </template>
                                                            </v-text-field>
                                                        </v-form>

                                                        <v-divider></v-divider>
                                                        
                                                        <v-layout row class="pa-2">
                                                            <v-container style="height: 200px;" class="pa-2 ma-2 overflow-y-auto">
                                                                <v-row 
                                                                    v-for="(answer, index) in editedItem.answers" 
                                                                    class="pa-0 ma-0"
                                                                >
                                                                    <v-row class="pa-0 ma-0" v-if="editedAnswerIndex == index">
                                                                        <v-col cols="11">
                                                                            <v-text-field 
                                                                                v-model="editedItem.answers[index]"
                                                                                underlined
                                                                                flat
                                                                                dense
                                                                                height="20px"
                                                                                hide-details="auto"
                                                                            >
                                                                            </v-text-field>
                                                                        </v-col>
                                                                        <v-col class="text-right" cols="1">
                                                                            <v-icon @click.stop="saveAnswer(index)">
                                                                                done
                                                                            </v-icon>
                                                                        </v-col>
                                                                    </v-row>

                                                                    <v-row class="pa-0 ma-0" v-else style="width: 100%;">
                                                                        <v-col v-text="answer" cols="10"></v-col>
                                                                        <v-col class="text-right" cols="1">
                                                                            <v-icon @click.stop="updateAnswer(index)">
                                                                                edit
                                                                            </v-icon>
                                                                        </v-col>
                                                                        <v-col class="text-right" cols="1">
                                                                            <v-icon @click.stop="deleteAnswer(index)" :disabled="editedAnswerIndex != -1">
                                                                                delete
                                                                            </v-icon>
                                                                        </v-col>
                                                                    </v-row>
                                                                
                                                                </v-row>
                                                            </v-container>
                                                        </v-layout>
                                                    </v-col>
                                                </v-card>

                                                <v-switch label="Buttons" v-model="buttonSwitch"></v-switch>

                                                <v-card flat class="ma-1" outlined v-if="buttonSwitch">
                                                    <v-col class="pa-0 ma-0">
                                                        <v-form v-model="valid" class="pa-2">
                                                            <v-text-field v-model="editedItem.new_button_name" label="Button Name"
                                                                prepend-icon="smart_button" :counter="200">
                                                            </v-text-field>
                                                            <v-text-field v-model="editedItem.new_button_answer" label="Button Answer"
                                                                prepend-icon="question_answer" :counter="200">
                                                                <template #append>
                                                                    <v-btn icon class="mb-1" color="gray"
                                                                        @click="addNewButton" :disabled="editedItem.new_button_name.length == 0 || editedItem.new_button_answer.length == 0">
                                                                        <v-icon>mdi-plus</v-icon>
                                                                    </v-btn>
                                                                </template>
                                                            </v-text-field>
                                                        </v-form>

                                                        <v-divider></v-divider>

                                                        <v-layout row class="pa-2">
                                                            <v-container>
                                                                <v-list
                                                                    style="height: 200px"
                                                                    class="overflow-y-auto"
                                                                    dense
                                                                    two-line
                                                                >
                                                                    <v-list-item
                                                                        v-for="button in editedItem.buttons"
                                                                        :key="index"
                                                                        height="1"
                                                                    >

                                                                        <v-list-item-content>
                                                                            <v-list-item-title v-text="button.text"></v-list-item-title>
                                                                            <v-list-item-title v-text="button.answer[0]"></v-list-item-title>
                                                                        </v-list-item-content>

                                                                        <v-list-item-action>
                                                                            <v-icon @click.stop="updateItem(index)">
                                                                                edit
                                                                            </v-icon>
                                                                        </v-list-item-action>

                                                                    </v-list-item>
                                                                </v-list>
                                                            </v-container>
                                                        </v-layout>
                                                    </v-col>
                                                </v-card>

                                            </v-container>

                                        </v-card-text>

                                        <v-card-actions>
                                            <v-spacer></v-spacer>
                                            <v-btn color="blue darken-1" text @click="close">
                                                İptal
                                            </v-btn>
                                            <v-btn color="blue darken-1" text @click="save" :disabled="editedItem.questions.length == 0 || editedItem.answers.length == 0">
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

            answerRules: [
                v => !!v || 'answer is required',
            ],

            questionRules: [
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
                new_answer: '',
                new_button_name: '',
                new_button_answer: '',
                questions: [],
                answers: [],
                buttons: [],
                category: '',
            },

            defaultItem: {
                new_question: '',
                new_answer: '',
                new_button_name: '',
                new_button_answer: '',
                questions: [],
                answers: [],
                buttons: [],
                category: '',
            },

            buttonSwitch: false,
            editedQuestionIndex: -1,
            editedAnswerIndex: -1,
        }
    },
    mounted() {
        this.socketIoSocket = io();
        this.initialize();
    },
    computed: {
        formTitle() {
            return this.editedIndex === -1 ? 'Yeni Soru' : 'Soru Düzenle'
        }
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
            this.editedItem.questions.push(this.editedItem.new_question)
            this.editedItem.new_question = ""
        },

        addNewAnswer() {
            this.editedItem.answers.push(this.editedItem.new_answer)
            this.editedItem.new_answer = ""
        },

        addNewButton() {
            this.editedItem.buttons.push({"text": this.editedItem.new_button_name, "answer": [this.editedItem.new_button_answer]})
            this.editedItem.new_button_answer = ""
            this.editedItem.new_button_name = ""
        },

        updateQuestion(index) {
            this.editedQuestionIndex = index
        },

        saveQuestion(index) {
            this.editedQuestionIndex = -1
        },

        deleteQuestion(index) {
            this.editedItem.questions.splice(index, 1)
        },

        updateAnswer(index) {
            this.editedAnswerIndex = index
        },

        saveAnswer(index) {
            this.editedAnswerIndex = -1
        },

        deleteAnswer(index) {
            this.editedItem.answers.splice(index, 1)
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
            if (this.editedIndex > -1) {
                Object.assign(this.qa_pairs[this.editedIndex], this.editedItem);
                if (this.editedItem.question !== "" && this.editedItem.answer !== "" && this.editedItem.category !==
                        "") {
                    this.valid = false;
                } //What does this if do?

                axios.post('/updateQuestion', {id: this.editedItem.id,
                                               question: this.editedItem.question, // TODO: MAKE SURE THAT question AND answer ARE ARRAYS
                                               answer: this.editedItem.answer,
                                               category: this.editedItem.category}).catch(error => {
                console.log(error);
                }).then(response => {
                    this.qa_pairs[this.editedIndex].id = response.data.data
                    this.close() //TODO: ADD LOADING STUFF WHILE WAITING RESPONSE
                })
            }
            else {
                axios.post('/addQuestion', {question: this.editedItem.question,
                                            answer: this.editedItem.answer,
                                            category: this.editedItem.category}).catch(error => {
                console.log(error);
                }).then(response => {
                    this.editedItem.id = response.data.data
                    this.qa_pairs.push(this.editedItem)
                    this.close() //TODO: ADD LOADING STUFF WHILE WAITING RESPONSE
                })
            }
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
