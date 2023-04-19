<template>
	<div class="app">
		<Signup/>
		<router-view class="content"/>
	</div>
</template>

<script setup>
import Signup from '@/components/AdminSignup.vue';
</script>

<script>
export default {
  name: "AdminSignupView"
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

.signup{

	margin: auto;
	justify-content: center;
}

</style>
