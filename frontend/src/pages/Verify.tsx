import { useState } from 'react'
import { verifyOnChain } from '../api/submissions'

export default function Verify() {
	const [wallet, setWallet] = useState('')
	const [records, setRecords] = useState<any[]>([])
	const [error, setError] = useState('')

	async function verify() {
		setError('')
		try {
			const res = await verifyOnChain(wallet)
			setRecords(res.records || [])
		} catch (e: any) {
			setError(e?.response?.data?.detail || 'Failed to fetch on-chain records')
		}
	}

	return (
		<div className="space-y-4">
			<h2 className="text-2xl font-semibold">Verify On-Chain</h2>
			<div className="flex gap-2 items-center">
				<input value={wallet} onChange={e => setWallet(e.target.value)} placeholder="0x..." className="border rounded p-2 w-full md:w-96"/>
				<button onClick={verify} className="px-3 py-2 bg-gray-200 rounded">Search</button>
			</div>
			{error && <p className="text-red-600">{error}</p>}
			<ul className="space-y-2">
				{records.map((r, i) => (
					<li key={i} className="bg-white p-3 rounded shadow">
						<div className="flex gap-4 text-sm">
							<span className="font-semibold">Skill:</span> <span>{r.skill}</span>
							<span className="font-semibold">Score:</span> <span>{r.score}%</span>
							<span className="font-semibold">Timestamp:</span> <span>{new Date(r.timestamp * 1000).toISOString()}</span>
						</div>
					</li>
				))}
			</ul>
		</div>
	)
}