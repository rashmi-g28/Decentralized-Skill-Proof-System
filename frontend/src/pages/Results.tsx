import { useState } from 'react'
import { fetchResult, certificateUrl, pushOnChain } from '../api/submissions'

export default function Results() {
	const [resultId, setResultId] = useState('')
	const [data, setData] = useState<any>(null)
	const [error, setError] = useState('')
	const [pushing, setPushing] = useState(false)

	async function load() {
		setError('')
		try {
			const res = await fetchResult(Number(resultId))
			setData(res)
		} catch (e: any) {
			setError(e?.response?.data?.detail || 'Failed to fetch result')
		}
	}

	async function push() {
		setPushing(true)
		try {
			const res = await pushOnChain(Number(resultId))
			await load()
		} catch (e: any) {
			setError(e?.response?.data?.detail || 'Failed to push on-chain')
		} finally {
			setPushing(false)
		}
	}

	return (
		<div className="space-y-4">
			<h2 className="text-2xl font-semibold">Results</h2>
			<div className="flex gap-2 items-center">
				<input value={resultId} onChange={e => setResultId(e.target.value)} placeholder="Result ID" className="border rounded p-2"/>
				<button onClick={load} className="px-3 py-2 bg-gray-200 rounded">Load</button>
			</div>
			{error && <p className="text-red-600">{error}</p>}
			{data && (
				<div className="bg-white rounded shadow p-4 space-y-2">
					<p><span className="font-semibold">Skill:</span> {data.skill}</p>
					<p><span className="font-semibold">Score:</span> {data.score}%</p>
					<p><span className="font-semibold">Passed:</span> {String(data.passed)}</p>
					<p><span className="font-semibold">Tx Hash:</span> {data.blockchain_tx_hash || '—'}</p>
					<div className="flex gap-2">
						<a className="px-3 py-2 bg-blue-600 text-white rounded" href={certificateUrl(Number(resultId))}>Download Certificate</a>
						{!data.blockchain_tx_hash && data.passed && (
							<button className="px-3 py-2 bg-green-600 text-white rounded disabled:opacity-50" onClick={push} disabled={pushing}>{pushing ? 'Pushing...' : 'Push On-Chain'}</button>
						)}
					</div>
				</div>
			)}
		</div>
	)
}