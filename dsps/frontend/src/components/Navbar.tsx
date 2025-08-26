import { Link } from 'react-router-dom'

export default function Navbar() {
	return (
		<nav className="bg-white shadow">
			<div className="max-w-4xl mx-auto px-4 py-3 flex items-center justify-between">
				<Link to="/" className="font-semibold text-lg">DSPS</Link>
				<div className="space-x-4 text-sm">
					<Link className="hover:underline" to="/upload">Upload</Link>
					<Link className="hover:underline" to="/results">Results</Link>
					<Link className="hover:underline" to="/verify">Verify</Link>
				</div>
			</div>
		</nav>
	)
}