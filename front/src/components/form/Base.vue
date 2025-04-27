<template>
    <form @submit.prevent="handleSubmit" class="max-w-xl mx-auto bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-2xl font-semibold mb-6 text-gray-800">{{ props.title }}</h2>
        <h3 class="text-l font-semibold text-gray-800">{{ props.description }}</h3>

        <!-- Slot for custom fields -->
        <slot />

        <!-- Submit Button -->
        <div class="mt-6 flex justify-end gap-4">
            <!-- <button type="button"
                class="bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 transition" @click="ToggleUpdate">
                Update
            </button> -->
            <button type="button"
                class="bg-gray-300 text-gray-800 py-2 px-4 rounded-md hover:bg-gray-400 transition" @click="() => router.back()">
                Cancel
            </button>

            <button type="submit"
                class="bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition">
                Submit
            </button>
        </div>

    </form>
</template>

<script setup lang="ts">
const emit = defineEmits(['submit'])
const router = useRouter()

function handleSubmit() {
    emit('submit')
    router.back()
}

function ToggleUpdate() {
    isEditing.value = !isEditing.value
}

const props = defineProps({
    title: {
        type: [String],
        default: 'Title Form',
    },
    description: {
        type: [String],
        default: 'Description Form',
    },
    update: {
        type: Boolean,
        default: false,
    }
})
const isEditing = ref<boolean>(props.update)

</script>

  