"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { signupUser } from "@/lib/api";

export default function SignupPage() {
  const router = useRouter();
  const [form, setForm] = useState({ username: "", email: "", password: "" });
  const [error, setError] = useState("");

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      await signupUser(form);
      router.push("/login");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50">
      <form
        onSubmit={handleSubmit}
        className="bg-white p-8 rounded-xl shadow-md w-80 space-y-4"
      >
        <h2 className="text-2xl font-bold text-center">Sign Up</h2>
        {error && <p className="text-red-600 text-sm">{error}</p>}
        <input
          type="text"
          name="username"
          placeholder="Username"
          onChange={handleChange}
          className="w-full border border-gray-300 rounded-lg p-2"
        />
        <input
          type="email"
          name="email"
          placeholder="Email"
          onChange={handleChange}
          className="w-full border border-gray-300 rounded-lg p-2"
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          onChange={handleChange}
          className="w-full border border-gray-300 rounded-lg p-2"
        />
        <button
          type="submit"
          className="w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700"
        >
          Create Account
        </button>
        <p className="text-center text-sm">
          Already have an account?{" "}
          <a href="/login" className="text-blue-600 font-medium">
            Log In
          </a>
        </p>
      </form>
    </div>
  );
}
