import { useState } from 'react'
import { submitCode } from '../api/submissions'

export default function Upload() {
	const [userName, setUserName] = useState('')
	const [wallet, setWallet] = useState('')
	const [skill, setSkill] = useState('fibonacci')
	const [file, setFile] = useState<File | null>(null)
	const [loading, setLoading] = useState(false)
	const [result, setResult] = useState<any>(null)
	const [error, setError] = useState('')

	async function onSubmit(e: React.FormEvent) {
		e.preventDefault()
		if (!file) return
		setLoading(true)
		setError('')
		try {
			const data = await submitCode({ user_name: userName, wallet_address: wallet || undefined, skill, file })
			setResult(data)
		} catch (err: any) {
			setError(err?.response?.data?.detail || 'Upload failed')
		} finally {
			setLoading(false)
		}
	}

	return (
		<div className="space-y-6">
			<h2 className="text-2xl font-semibold">Upload Code</h2>
			<form onSubmit={onSubmit} className="space-y-4 bg-white p-4 rounded shadow">
				<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
					<label className="block">
						<span className="text-sm">Your Name</span>
						<input value={userName} onChange={e => setUserName(e.target.value)} className="mt-1 w-full border rounded p-2" required/>
					</label>
					<label className="block">
						<span className="text-sm">Wallet Address (optional)</span>
						<input value={wallet} onChange={e => setWallet(e.target.value)} className="mt-1 w-full border rounded p-2" placeholder="0x..."/>
					</label>
				</div>
				<label className="block">
					<span className="text-sm">Skill</span>
					<select value={skill} onChange={e => setSkill(e.target.value)} className="mt-1 w-full border rounded p-2">
						<option value="fibonacci">Fibonacci</option>
						<option value="palindrome">Palindrome</option>
					</select>
				</label>
				<label className="block">
					<span className="text-sm">Python File (.py)</span>
					<input type="file" accept=".py" onChange={e => setFile(e.target.files?.[0] || null)} className="mt-1 w-full" required/>
				</label>
				<button disabled={loading || !file} className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50">{loading ? 'Evaluating...' : 'Submit'}</button>
			</form>
			{error && <p className="text-red-600">{error}</p>}
			{result && (
				<div className="bg-white rounded shadow p-4 space-y-2">
					<div className="flex justify-between"><span className="font-semibold">Score</span><span>{result.score}%</span></div>
					<div className="flex justify-between"><span className="font-semibold">Passed</span><span>{String(result.passed_overall)}</span></div>
					<div>
						<p className="font-semibold">Details</p>
						<ul className="list-disc ml-6 text-sm">
							{result.details.map((d: any, i: number) => (
								<li key={i}><span className={d.pass ? 'text-green-700' : 'text-red-700'}>{d.case}: {String(d.pass)}</span></li>
							))}
						</ul>
					</div>
				</div>
			)}
		</div>
	)
}