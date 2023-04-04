<template>
    <div>
        <!--        <admin-bar />-->
        <admin-chart-pie></admin-chart-pie>

    </div>
</template>

<script>
import AdminBar from './AdminBar.vue'
import AdminChartPie from '@/components/AdminChartPie.vue';

export default {
    name: 'AdminChart',
    components: {
        AdminChartPie,
        AdminBar,
    },
}
</script>

