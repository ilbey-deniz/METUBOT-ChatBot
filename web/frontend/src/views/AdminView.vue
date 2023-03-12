<template>
	<div class="app">
		<!-- Sidebar -->
		<!-- <Sidebar style="min-width: 64px;"/> -->
		<div class="login" v-if="!is_logged_in">
			<!-- <Login/> -->
			<v-form class="px-12  py-12" style="background-color: rgb(220,200,220); border-radius: 25px" v-model="valid">
  			  <v-text-field v-model="username" label="username" prepend-icon="person"
  			  :rules="usernameRules" :counter="20" required></v-text-field>
  			  <v-text-field v-model="e_mail" label="e_mail" prepend-icon="mail"
  			  :rules="e_mailRules" :counter="20" required></v-text-field>  <!-- e_mail_mark may also be used -->
  			  <v-text-field v-model="password" label="password" prepend-icon="key" type="password"
  			  :rules="passwordRules" :counter="20" required></v-text-field>
  			  <v-spacer></v-spacer>
  			  <v-btn flat @click="submit" :disabled="!valid" class="primary mx-0 mt-3">Log In</v-btn>
  			</v-form>
		</div>

		<Sidebar v-if="is_logged_in" />

		<!-- Content -->

		<router-view class="content"/>
	</div>
</template>

<script setup>
import Sidebar from '../components/Sidebar.vue'
// import Login from '@/components/Login.vue';
</script>

<script>
export default {
  name: "AdminView",
//   components: {
//         AdminView,
//   },

  data() {
    return {
        is_logged_in: false,
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
        // socketIoSocket: null

    }
  },
  mounted() {
	this.is_logged_in = false;
    // this.socketIoSocket = io();
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
			this.is_logged_in = true;
        }
    }
  }
}
</script>

<style lang="scss">
:root {
	--primary: #de4a4a;
	--primary-alt: #c52222;
	--grey: #64748b;
	--dark: #1e293b;
	--dark-alt: #334155;
	--light: #f1f5f9;
	--sidebar-width: 300px;
}
* {
	margin: 0;
	padding: 0;
	box-sizing: border-box;
	font-family: 'Fira sans', sans-serif;
}
body {
	background: var(--light);
}
button {
	cursor: pointer;
	appearance: none;
	border: none;
	outline: none;
	background: none;
}
.app {
	display: flex;
	height: 100%;

	main {

		flex: 1 1 0;
		padding: 2rem;
		@media (max-width: 1024px) {
			padding-left: calc(10rem - 64px);
		}
	}
}

.content{
	@media (max-width: 1024px) {
			margin-left: 64px;

		}
}

.login{

	margin: auto;
	justify-content: center;
}

</style>
