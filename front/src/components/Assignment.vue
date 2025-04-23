<template>
    <div class="flex items-center justify-between px-6 py-4 bg-white shadow-md">
        <!-- Left Column: Title Text -->
        <div class="text-xl font-bold text-gray-800">
            {{ title }}
        </div>

        <!-- Right Column: Button with 3 States -->
        <div>
            <button :class="{
                'px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600': props.status === StatusType.SUBMIT,
                'px-4 py-2 bg-blue-300 text-white rounded cursor-wait': props.status === StatusType.PANDING,
                'px-4 py-2 bg-gray-500 text-white rounded cursor-not-allowed': props.status === StatusType.WAITING
            }" :disabled="status === StatusType.PANDING || props.status === StatusType.WAITING">
                <!-- Display loading text or default button text -->
                <span v-if="status === StatusType.PANDING">Loading...</span>
                <span v-else-if="status === StatusType.WAITING">Disabled</span>
                <span v-else>Details</span>
            </button>
        </div>
    </div>
</template>
  
<script setup lang="ts">
import { ref } from 'vue'

// States for button
enum StatusType {
    SUBMIT = 'submit',
    PANDING = 'panding',
    WAITING = 'waiting'
}

const props = defineProps({
    status: {
        type: String as () => StatusType,
        default: StatusType.PANDING,
    },
    title: {
        type: [String],
        default: 'Description Form',
    },
})

// const handleButtonClick = () => {
//     if (props.status === StatusType.SUBMIT) {
//         props.status = StatusType.PANDING
//         setTimeout(() => {
//             props.status = StatusType.WAITING
//         }, 2000) // Simulate a delay
//     }
// }
</script>
  