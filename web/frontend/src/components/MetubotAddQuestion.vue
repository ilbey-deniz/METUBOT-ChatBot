<template>
  <v-form class="px-12  py-12" v-model="valid"> 
    <v-text-field v-model="category" label="Category" prepend-icon="category" 
    :rules="categoryRules" :counter="30" required></v-text-field>
    <v-textarea v-model="question" label="Question" prepend-icon="quiz" 
    :rules="questionRules" :counter="200" required></v-textarea>  <!-- question_mark may also be used -->
    <v-textarea v-model="answer" label="Answer" prepend-icon="edit_note"
    :rules="answerRules" :counter="200" required></v-textarea>
    <v-spacer></v-spacer>
    <v-btn flat @click="submit" :disabled="!valid" class="error mx-0 mt-3">Add Q/A</v-btn>
  </v-form>
</template> 

<script>
// import axios from 'axios'
// import Vue from 'vue'
import { io } from "socket.io-client";

export default {
  data() {
    return {
        valid: false,
        category: '',
        question: '',
        answer: '',
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
        socketIoSocket: null
    }
  },
  mounted() {
    this.socketIoSocket = io();
  },
  methods: {
    submit() {
      console.log(this.category, this.question, this.answer)
      if (this.category !== "" && this.answer !== "" && this.question !== "") {
            let snd_data = {
                "category": this.category,
                "question": this.question, 
                "answer": this.answer
            }
            console.log(snd_data)
            this.socketIoSocket.emit('add question', snd_data);
            this.valid = false;
            this.category = '';
            this.question = '';
            this.answer = '';
            // this.waitingForAnswer = true;
        }
    }
  }
}
</script>