<template>
    <metubot-chat :app-bar-height="appBarHeight"/>
</template>

<script>
import MetubotChat from '../components/MetubotChat'

export default {
    name: 'Home',
    props: {
        appBarHeight: Number,
    },
    components: {
        MetubotChat,
    },
}
</script>

<style scoped>



</style>
