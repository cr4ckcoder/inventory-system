"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { loginUser } from "@/lib/api";
import { setToken } from "@/lib/auth";

export default function LoginPage() {
  const router = useRouter();
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const res = await loginUser(form);
      if (res?.access_token) {
        setToken(res.access_token);
        router.push("/dashboard");
      } else {
        setError("Invalid credentials");
      }
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
        <h2 className="text-2xl font-bold text-center">Login</h2>
        {error && <p className="text-red-600 text-sm">{error}</p>}
        <input
          type="text"
          name="username"
          placeholder="Username"
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
          className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700"
        >
          Sign In
        </button>
        <p className="text-center text-sm">
          Don’t have an account?{" "}
          <a href="/signup" className="text-blue-600 font-medium">
            Sign Up
          </a>
        </p>
      </form>
    </div>
  );
}
