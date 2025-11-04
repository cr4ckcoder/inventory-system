
import Link from "next/link";

export default function HomePage() {
  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <div className="bg-white p-8 rounded-2xl shadow-md text-center space-y-4">
        <h1 className="text-4xl font-bold text-gray-900">Inventory System</h1>
        <p className="text-gray-600">Welcome to the Central Inventory Dashboard</p>
        <Link
          href="/login"
          className="inline-block px-6 py-2 text-white bg-blue-600 hover:bg-blue-700 rounded-lg font-medium"
        >
          Get Started
        </Link>
      </div>
    </div>
  );
}
