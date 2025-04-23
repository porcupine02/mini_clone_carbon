<template>
  <div class="flex flex-col mb-4 p-2">
    <label v-if="label" :for="id" class="mb-1 text-m font-medium text-gray-700">
      {{ label }}
    </label>
    <input :id="id" type="file" @change="handleFileChange" :disabled="!edit"
      class="px-4 py-2 text-base border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100" />
  </div>
</template>
  
<script setup>
const emit = defineEmits(['update:file'])

defineProps({
  label: {
    type: String,
    default: '',
  },
  id: {
    type: String,
    default: 'file-upload-field',
  },
  edit: {
    type: Boolean,
    default: true,
  },
})

function handleFileChange(event) {
  const file = event.target.files[0]
  emit('update:file', file)
}
</script>
  