import { Link } from 'react-router-dom'

export default function Home() {
	return (
		<div className="space-y-6">
			<h1 className="text-3xl font-bold">Decentralized Skill Proof System</h1>
			<p className="text-gray-700">Submit code challenges, get scored, and mint a tamper-proof proof of skill on-chain.</p>
			<div className="flex gap-3">
				<Link to="/upload" className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Submit Code</Link>
				<Link to="/verify" className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300">Verify Wallet</Link>
			</div>
		</div>
	)
}