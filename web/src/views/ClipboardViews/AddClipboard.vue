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
                    <el-form-item label="权限">
                        <el-select v-model="clipboardForm.permission" style="width: 240px">
                            <el-option v-for="item in permissionOptions" :key="item.value" :label="item.label"
                                :value="item.value" />
                        </el-select>
                    </el-form-item>
                    <el-form-item label="内容">
                        <el-input v-model="clipboardForm.content" :autosize="{ minRows: 10 }"
                            type="textarea"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="addClipboard">添加</el-button>
                    </el-form-item>
                </el-form>
            </el-card>
        </el-col>
    </el-row>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue';
import { ElMessage, type FormInstance } from 'element-plus';
import { addClipboardApi } from '@/apis/clipboardApis';

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
    title: '',
    permission: '',
    content: '',
});

const clipboardFormRef = ref<FormInstance>();

async function addClipboard() {
    console.log(clipboardForm);
    const res = await addClipboardApi(clipboardForm);
    if (res.code === 0) {
        ElMessage.success('添加成功');
    }
}

</script>