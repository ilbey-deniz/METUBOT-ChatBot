<template>
  <div class="login">
			<!-- <Login/> -->
			<v-form class="px-12  py-12" style="background-color: rgb(220,200,220); border-radius: 25px" v-model="valid">
  			  <v-text-field v-model="e_mail" label="email" prepend-icon="mail"
  			  :rules="e_mailRules" :counter="20" required></v-text-field>  <!-- e_mail_mark may also be used -->
  			  <v-text-field v-model="password" label="password" prepend-icon="key" type="password"
  			  :rules="passwordRules" :counter="20" required></v-text-field>
          <v-text class="mt-2" v-show="no_such_user || wrong_password">
            <p class="text-body-2" >Wrong email or password.</p>
          </v-text>
          <v-text class="mt-2" v-show="missing_credentials">
            <p class="text-body-2" >Missing credentials.</p>
          </v-text>
  			  <v-spacer></v-spacer>
  			  <v-btn text @click="submit" :disabled="!valid" class="primary mx-0 mt-3">Log In</v-btn>
			  <div class="mt-2">
                <p class="text-body-2">Don't have an account? <a href="#/signup">Sign Up</a></p>
              </div>
  			</v-form>
		</div>
</template>

<script>
import { io } from "socket.io-client";


export default {
  name: "Login",
  data() {
    return {
        valid: false,
        e_mail: '',
        password: '',
        missing_credentials: false,
        wrong_password: false,
        no_such_user: false,

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
  beforeMount(){
    this.socketIoSocket = io();
    this.token = localStorage.getItem("token");
      if (this.token !== null) {
        this.socketIoSocket.emit('token check', this.token);
        this.socketIoSocket.on("token check answer", (data) => {
          if(data["status"] == "success"){
            this.$router.push("/yonetim");
          }
          else{
            this.$router.push("/login");
          }
        })
      }
      else{
        this.$router.push("/login");
      }
    
  },
  mounted() {
  
    this.socketIoSocket.on("login answer", (data) => {
      if (data["status"] === "success") {
        localStorage.setItem("token", data["token"]);
        this.$router.push("/yonetim");
        
      }
      else{
            if(data["message"] === "noSuchUser"){
                this.no_such_user = true;
                setTimeout(() => {
                    this.no_such_user = false;
                }, 5000);
            }
            else if(data["message"] === "missingCredentials"){
                this.missing_credentials = true;
                setTimeout(() => {
                    this.missing_credentials = false;
                }, 5000);
            }
            else if(data["message"] === "wrongPassword"){
                this.wrong_password = true;
                setTimeout(() => {
                    this.wrong_password = false;
                }, 5000);
            }
        }
      })
  },
  methods: {
    submit() {
      if (this.password !== "" && this.e_mail !== "") {
            let check_data = {
                "mail": this.e_mail,
                "password": this.password
            }
            this.valid = false;
            this.socketIoSocket.emit('login', check_data);
        }
    }
  }
}
</script>
