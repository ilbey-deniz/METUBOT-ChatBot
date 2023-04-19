<template>
    <div class="signup">
              <!-- <Signup/> -->
              <v-form class="px-12  py-12" style="background-color: rgb(220,200,220); border-radius: 25px" v-model="valid">
                  <v-text-field v-model="username" label="username" prepend-icon="person"
                  :rules="usernameRules" :counter="20" required></v-text-field>
                  <v-text-field v-model="e_mail" label="email" prepend-icon="mail"
                  :rules="e_mailRules" :counter="20" required></v-text-field>  <!-- e_mail_mark may also be used -->
                  <v-text-field v-model="password" label="password" prepend-icon="key" type="password"
                  :rules="passwordRules" :counter="20" required></v-text-field>
                  <v-text-field v-model="passwordMatch" label="re-enter password" prepend-icon="key" type="password"
                  :rules="passwordMatchRules" :counter="20" required></v-text-field>
                  <div class="mt-2" v-show="user_exists">
                    <p class="text-body-2" >User with specified email already exists.</p>
                  </div>
                  <div class="mt-2">
                    <p class="text-body-2">Already have an account? <a href="#/login">Login</a></p>
                  </div>
                  <v-spacer></v-spacer>
                  <v-btn text @click="submit" :disabled="!valid" class="primary mx-0 mt-3">SIGN UP</v-btn>
                </v-form>
          </div>
</template>
  
<script>
import { io } from "socket.io-client";
  
  
  export default {
    name: "Signup",
    data() {
      return {
          valid: false,
          username: '',
          e_mail: '',
          password: '',
          passwordMatch: '',
          user_exists: false,
          missing_credentials: false,
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
          passwordMatchRules: [
              v => !!v || 'password needs to be re-entered',
              v => v === this.password || 'passwords must match',
          ],
          socketIoSocket: null
      }
    },
    beforeMount() {
      this.socketIoSocket = io();
      this.token = localStorage.getItem("token");
        if (this.token !== null) {
          this.socketIoSocket.emit('token check', this.token);
          this.socketIoSocket.on("token check answer", (data) => {
            if(data["status"] === "success"){
              this.$router.push("/yonetim");
            }
            else{
              this.$router.push("/signup");
            }
          })
        }
        else{
          this.$router.push("/signup");
        }
      
    },
    mounted() {
        this.socketIoSocket.on("register answer", (data) => {
        if (data["status"] === "success") {
            localStorage.setItem("token", data["token"]);
            this.$router.push("/yonetim");
        }
        else{
            if(data["message"] === "userExists"){
                this.user_exists = true;
                setTimeout(() => {
                    this.user_exists = false;
                }, 5000);
            }
            else if(data["message"] === "missingCredentials"){
                this.missing_credentials = true;
                setTimeout(() => {
                    this.missing_credentials = false;
                }, 5000);
            }
        }
        })
      
    },
    methods: {
      submit() {
        if (this.username !== "" && this.password !== "" && this.e_mail !== "") {
              let check_data = {
                  "username": this.username,
                  "mail": this.e_mail,
                  "password": this.password
              }
              this.socketIoSocket.emit('register', check_data);
        }
      }
        
    }
  }
  </script>
  