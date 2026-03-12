<template>
    <el-row :span="24">
        <h1>Add Clipboard</h1>
    </el-row>
    <el-row>
        <el-col :span="12" :offset="6">
            <el-card>
                <el-form ref="clipboardFormRef" :model="clipboardForm" size="large" label-position="top">
                    <el-form-item label="标题">
                        <el-input v-model="clipboardForm.title"></el-input>
                    </el-form-item>
                    <el-form-item v-if="userInfo?.id === clipboardForm.user" label="权限">
                        <el-select v-model="clipboardForm.permission" style="width: 240px">
                            <el-option v-for="item in permissionOptions" :key="item.value" :label="item.label"
                                :value="item.value" />
                        </el-select>
                    </el-form-item>
                    <el-form-item label="内容">
                        <el-input v-model="clipboardForm.text_content" :autosize="{ minRows: 10 }"
                            type="textarea"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="saveClipboard">保存</el-button>
                    </el-form-item>
                </el-form>
            </el-card>
        </el-col>
    </el-row>
</template>
<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { getClipboardApi, editClipboardApi } from '@/apis/clipboardApis';
import { useUserStore } from '@/stores/user';
import type { FormInstance } from 'element-plus';
import { id } from 'element-plus/es/locales.mjs';

const permissionOptions = [
    {
        value: 'publish',
        label: '公开',
    },
    {
        value: 'private',
        label: '私有',
    },
    {
        value: 'shared_password',
        label: '密码共享',
    },
];

const clipboardForm = reactive({
    id: null,
    title: '',
    permission: 'public',
    text_content: '',
    user: null,
});

const clipboardFormRef = ref<FormInstance>();

const userInfo = useUserStore().getUser();

async function saveClipboard() {
    if (clipboardFormRef.value?.validate() && clipboardForm.id) {
        editClipboardApi(clipboardForm.id, clipboardForm);
    }
    // if (res.code === 0) {
    //     router.push('/');
    // }
}

onMounted(() => {
    getClipboardApi("3f76c4bf-7685-4342-a637-b277925d16e6").then(res => {
        if (res.code === 0) {
            clipboardForm.id = res.data.id;
            clipboardForm.title = res.data.title;
            clipboardForm.permission = res.data.permission;
            clipboardForm.text_content = res.data.text_content;
            clipboardForm.user = res.data.user;
        }
    })
    console.log('edit clipboard');
});

</script>