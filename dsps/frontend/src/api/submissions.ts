import { api } from './client'

export async function submitCode(params: { user_name: string; wallet_address?: string; skill: string; file: File }) {
	const form = new FormData()
	form.append('user_name', params.user_name)
	if (params.wallet_address) form.append('wallet_address', params.wallet_address)
	form.append('skill', params.skill)
	form.append('file', params.file)
	const res = await api.post('/api/v1/submit', form, { headers: { 'Content-Type': 'multipart/form-data' } })
	return res.data
}

export async function fetchResult(resultId: number) {
	const res = await api.get(`/api/v1/results/${resultId}`)
	return res.data
}

export function certificateUrl(resultId: number) {
	return `${api.defaults.baseURL}/api/v1/certificates/${resultId}`
}

export async function pushOnChain(resultId: number) {
	const res = await api.post(`/api/v1/results/${resultId}/push`)
	return res.data
}

export async function verifyOnChain(wallet: string) {
	const res = await api.get(`/api/v1/verify/${wallet}`)
	return res.data
}