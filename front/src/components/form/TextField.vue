<template>
  <div class="flex flex-col mb-4 p-2">
    <label v-if="label" :for="id" class="mb-1 text-m font-medium text-gray-700">
      {{ label }}
    </label>
    <input :id="id" :value="modelValue" @input="$emit('update:modelValue', $event.target.value)"
      :placeholder="placeholder" :type="type" :disabled="!edit"
      class="px-4 py-2 text-base border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500" />
  </div>
</template>
  
<script setup>
defineProps({
  modelValue: {
    type: [String, Number],
    default: '',
  },
  label: {
    type: String,
    default: '',
  },
  placeholder: {
    type: String,
    default: '',
  },
  id: {
    type: String,
    default: 'text-field-input',
  },
  type: {
    type: String,
    default: 'text',
  },
  edit: {
    type: Boolean,
    default: true,
  },
})

defineEmits(['update:modelValue'])
</script>
  