import React, { useState, useEffect } from "react";
import axios from "axios";

interface PortfolioItem {
  symbol: string;
  quantity: number;
  purchase_price: number;
  current_price: number;
}

interface Portfolio {
  user_id: string;
  items: PortfolioItem[];
  total_value?: number;
}

export const PortfolioComponent: React.FC = () => {
  const [portfolio, setPortfolio] = useState<Portfolio | null>(null);
  const [loading, setLoading] = useState(false);
  const [userId, setUserId] = useState("user-001");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchPortfolio();
  }, [userId]);

  const fetchPortfolio = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(`/api/portfolio/${userId}`);
      setPortfolio(response.data.portfolio);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to fetch portfolio");
    } finally {
      setLoading(false);
    }
  };

  const calculateTotal = (): number => {
    if (!portfolio) return 0;
    return portfolio.items.reduce(
      (sum, item) => sum + item.quantity * item.current_price,
      0,
    );
  };

  const calculateGain = (item: PortfolioItem): number => {
    return (item.current_price - item.purchase_price) * item.quantity;
  };

  return (
    <div className="portfolio-container p-6">
      <h1 className="text-2xl font-bold mb-4">Portfolio Overview</h1>

      <div className="user-selector mb-4">
        <input
          type="text"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          placeholder="Enter User ID"
          className="border px-3 py-2 rounded"
        />
        <button
          onClick={fetchPortfolio}
          className="ml-2 bg-blue-500 text-white px-4 py-2 rounded"
          disabled={loading}
        >
          {loading ? "Loading..." : "Fetch"}
        </button>
      </div>

      {error && <div className="text-red-600 mb-4">{error}</div>}

      {portfolio && (
        <div className="portfolio-details">
          <div className="summary bg-gray-100 p-4 rounded mb-4">
            <p className="text-lg">
              Total Portfolio Value:{" "}
              <strong>${calculateTotal().toFixed(2)}</strong>
            </p>
            <p className="text-md">Holdings: {portfolio.items.length} assets</p>
          </div>

          <table className="w-full border-collapse border border-gray-300">
            <thead className="bg-gray-200">
              <tr>
                <th className="border p-2">Symbol</th>
                <th className="border p-2">Quantity</th>
                <th className="border p-2">Purchase Price</th>
                <th className="border p-2">Current Price</th>
                <th className="border p-2">Gain/Loss</th>
                <th className="border p-2">Total Value</th>
              </tr>
            </thead>
            <tbody>
              {portfolio.items.map((item, idx) => (
                <tr key={idx} className="hover:bg-gray-50">
                  <td className="border p-2">{item.symbol}</td>
                  <td className="border p-2">{item.quantity}</td>
                  <td className="border p-2">
                    ${item.purchase_price.toFixed(2)}
                  </td>
                  <td className="border p-2">
                    ${item.current_price.toFixed(2)}
                  </td>
                  <td
                    className={`border p-2 ${calculateGain(item) >= 0 ? "text-green-600" : "text-red-600"}`}
                  >
                    ${calculateGain(item).toFixed(2)}
                  </td>
                  <td className="border p-2">
                    ${(item.quantity * item.current_price).toFixed(2)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {!portfolio && !loading && !error && (
        <div className="text-gray-500">
          Enter a user ID and click Fetch to view portfolio
        </div>
      )}
    </div>
  );
};

export default PortfolioComponent;
