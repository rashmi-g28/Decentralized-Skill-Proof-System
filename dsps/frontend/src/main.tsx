import React from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import './styles/index.css'
import Home from './pages/Home'
import Upload from './pages/Upload'
import Results from './pages/Results'
import Verify from './pages/Verify'
import Navbar from './components/Navbar'

const router = createBrowserRouter([
	{ path: '/', element: <Home /> },
	{ path: '/upload', element: <Upload /> },
	{ path: '/results', element: <Results /> },
	{ path: '/verify', element: <Verify /> },
])

function App() {
	return (
		<div className="min-h-screen bg-gray-50 text-gray-900">
			<Navbar />
			<div className="max-w-4xl mx-auto p-4">
				<RouterProvider router={router} />
			</div>
		</div>
	)
}

ReactDOM.createRoot(document.getElementById('root')!).render(
	<React.StrictMode>
		<App />
	</React.StrictMode>
)