<template>
    <div class="p-6">
        <h2 class="text-2xl font-bold mb-4">Dashboard</h2>

        <div class="flex items-center space-x-4 mb-4">
            <!-- Subject -->
            <h2>Subject</h2>
            <select v-model="selectedSubject" class="border px-3 py-2 rounded">
                <option value="" disabled selected>Select Subject</option>
                <option v-for="subject in subjects" :key="subject.id" :value="subject">{{ subject.name }}</option>
            </select>

            <p>จำนวนโปรเจ็คทั้งหมด: <strong>{{ projectCount }}</strong> คน</p>
        </div>

        <BarChart :chart-data="chartData" :key="chartData"/>

        <div class="flex items-end space-x-4 my-4">
            <!-- Form -->
            <h2>Form</h2>
            <select v-model="selectedForm" class="border px-3 py-2 rounded">
                <option v-for="form in forms" :key="form.id" :value="form">{{ form.title }}</option>
            </select>
        </div>

        <div class="mt-8">
            <h3 class="text-lg font-semibold mb-2">Form in {{ selectedSubject?.name }}</h3>
            <table class="min-w-full border border-gray-300 text-sm">
                <thead class="bg-gray-100">
                    <tr>
                        <th class="px-4 py-2">ชื่อแบบฟอร์ม</th>
                        <th class="px-4 py-2">คำอธิบาย</th>
                        <th class="px-4 py-2">จำนวนการส่ง</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="form in forms" :key="form.id" class="border-t">
                        <td class="px-4 py-2">{{ form.title }}</td>
                        <td class="px-4 py-2">{{ form.description }}</td>
                        <td class="px-4 py-2">{{ form.submissions_count }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const user = ref()
const accessToken = ref()
const subjects = ref<SubjectResponse[]>([])
const projectCount = ref<number>(0)
const forms = ref<FormResponse[]>([])
const listForms = ref<FormResponse[]>([])

const selectedSubject = ref<SubjectResponse | null>(null)
const selectedForm = ref<FormResponse | null>(null)

const chartData = ref<chartType>({
    labels: [],
    datasets: [
        {
            label: 'Form Submissions',
            backgroundColor: '#10b981',
            data: [],
        },
    ],
})

const getAuth = async () => {
    accessToken.value = localStorage.getItem('access_token') ?? ''
    const rawUser = localStorage.getItem('user')
    user.value = rawUser ? JSON.parse(rawUser) : null
}

watch(selectedSubject, async(newValue, oldValue) => {
    if (newValue) {
        console.log('Subject selected:', newValue);
        await getFormBySubject(newValue.id);
        await getAllProjectBySubject()
    } else {
        console.log('No subject selected');
    }
});
const getFormBySubject = async (projectId: number) => {
    try {
        const res = await useFetch(
            `http://localhost:8000/form/subject/${projectId}/all-forms`,
            {
                method: 'GET',
                headers: {
                    Authorization: `Bearer ${accessToken.value}`,
                },
            }
        )
        if (res.data) {
            forms.value = res.data.value as FormResponse[];
            updateChartData(forms.value)
        }
    } catch (error) {
        console.error('Request failed:', error);
    }
}

const getAllSubjects = async () => {
    try {
        const res = await useFetch(
            'http://localhost:8000/form/subject',
            {
                method: 'GET',
                headers: {
                    Authorization: `Bearer ${accessToken.value}`,
                },
            }
        )
        subjects.value = res.data.value as SubjectResponse[];
    } catch (error) {
        console.error('Request failed:', error);
    }
}
const getAllProjectBySubject = async () => {
    try {
        const res = await useFetch<Project[]>(
            `http://localhost:8000/project/subject/${selectedSubject.value?.id}`,
            {
                method: 'GET',
                headers: {
                    Authorization: `Bearer ${accessToken.value}`,
                },
            }
        )
        const proj = res.data.value ?? []
        projectCount.value = proj.length
        console.log('coun', projectCount.value)
    } catch (error) {
        console.error('Request failed:', error);
    }
}

// const getAllForms = async () => {
//     try {
//         const res = await useFetch(
//             'http://localhost:8000/form',
//             {
//                 method: 'GET',
//                 headers: {
//                     Authorization: `Bearer ${accessToken.value}`,
//                 },
//             }
//         )
//         listForms.value = res.data.value as FormResponse[];
//         updateChartData(listForms.value);
//     } catch (error) {
//         console.error('Request failed:', error);
//     }
// }

const updateChartData = (forms: FormResponse[]) => {
    // chartData.value.labels = forms.map(form => form.title);
    // chartData.value.datasets[0].data = forms.map(form => form.submissions_count);
    chartData.value = {
        labels: forms.map(form => form.title),
        datasets: [
            {
                label: 'Form Submissions',
                backgroundColor: '#10b981',
                data: forms.map(form => form.submissions_count),
            }
        ]
    };
}

onMounted(async () => {
    await getAuth();
    await getAllSubjects();
    // await getAllProjectBySubject();
    // await getAllForms();
})

interface FormResponse {
    id: number;
    subjects: number[];
    title: string;
    description: string;
    main: string;
    created_at: string;
    updated_at: string;
    created_by: string;
    updated_by: string;
    submissions_count: number;
}

interface SubjectResponse {
    id: number;
    name: string;
    forms: FormResponse[];
    created_at: string;
    updated_at: string;
    created_by: string;
    updated_by: string;
}

interface chartType {
    labels: string[],
    datasets: {
        label: string,
        backgroundColor: string,
        data: number[]
    }[]
}
type Project = {
  id: number;
  subject: {
    id: number;
    name: string;
    forms: {
      id: number;
      title: string;
      description: string;
    }[];
  };
  student: {
    id: number;
    username: string;
  };
  title_th: string;
  title_en: string;
  keyword: string[];
};

</script>
