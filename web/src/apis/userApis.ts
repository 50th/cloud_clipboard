import request from '@/apis/axiosInstance'

const apiPrefix = '/api/user'

export async function loginApi(username: string, password: string): Promise<any> {
  return request.post(`${apiPrefix}/login/`, { username, password })
}

export async function checkAccessApi(token: string): Promise<any> {
  return request.post(`${apiPrefix}/token/verify/`, { token })
}
