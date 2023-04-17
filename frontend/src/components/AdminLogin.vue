<template>
  <v-form class="px-12  py-12" style="background-color: rgb(220,200,220); border-radius: 25px" v-model="valid">
  			  <v-text-field v-model="username" label="username" prepend-icon="person"
  			  :rules="usernameRules" :counter="20" required></v-text-field>
  			  <v-text-field v-model="e_mail" label="e_mail" prepend-icon="mail"
  			  :rules="e_mailRules" :counter="20" required></v-text-field>  <!-- e_mail_mark may also be used -->
  			  <v-text-field v-model="password" label="password" prepend-icon="key" type="password"
  			  :rules="passwordRules" :counter="20" required></v-text-field>
  			  <v-spacer></v-spacer>
  			  <v-btn text @click="submit" :disabled="!valid" class="primary mx-0 mt-3">Log In</v-btn>
			  <div class="mt-2">
                <p class="text-body-2">Don't have an account? <a href="#">Sign Up</a></p>
              </div>
  			</v-form>
</template>

<script>
// import axios from 'axios'
// import Vue from 'vue'
import { io } from "socket.io-client";


export default {
  name: "AdminLogin",
  data() {
    return {
        valid: false,
        username: '',
        e_mail: '',
        password: '',
        usernameRules: [
            v => !!v || 'username is required',
            v => v.length <= 20 || 'username must be less than 20 characters',
        ],

        e_mailRules: [
            v => !!v || 'e_mail is required',
            v => /.+@.+/.test(v) || 'E-mail must be valid',
        ],

        passwordRules: [
            v => !!v || 'password is required',
        ],
        socketIoSocket: null
    }
  },
  mounted() {
    this.socketIoSocket = io();
  },
  methods: {
    submit() {
      console.log(this.username, this.e_mail, this.password)
      if (this.username !== "" && this.password !== "" && this.e_mail !== "") {
            let check_data = {
                "username": this.username,
                "e_mail": this.e_mail,
                "password": this.password
            }
            console.log(check_data)
            // this.socketIoSocket.emit('add e_mail', check_data);
            this.valid = false;
            // this.username = '';
            // this.e_mail = '';
            // this.password = '';
            // this.waitingForpassword = true;
        }
    }
  }
}
</script>
