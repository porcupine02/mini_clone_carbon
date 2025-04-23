<template>
  <div class="flex flex-col mb-4 p-2">
    <label v-if="label" :for="id" class="mb-1 text-m font-medium text-gray-700">
      {{ label }}
    </label>
    <select :id="id" :value="modelValue" :disabled="!edit" @change="$emit('update:modelValue', $event.target.value)"
      class="px-4 py-2 text-base border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
      <option disabled value="">{{ placeholder }}</option>
      <option v-for="option in options" :key="option.value" :value="option.value">
        {{ option.label }}
      </option>
    </select>
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
    default: 'Select an option',
  },
  id: {
    type: String,
    default: 'select-field',
  },
  options: {
    type: Array,
    required: true,
    default: () => [],
  },
  edit: {
    type: Boolean,
    default: true,
  },
})

defineEmits(['update:modelValue'])
</script>
  