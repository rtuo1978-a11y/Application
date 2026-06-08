import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { ArrowLeft } from 'lucide-react';

const GuestRegistrationPage = () => {
  const navigate = useNavigate();
  const [tables, setTables] = useState([]);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    table_number: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchTables();
  }, []);

  const fetchTables = async () => {
    try {
      const { data } = await axios.get(`${process.env.REACT_APP_BACKEND_URL}/api/tables`);
      setTables(data);
    } catch (err) {
      console.error('Error fetching tables:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const { data } = await axios.post(
        `${process.env.REACT_APP_BACKEND_URL}/api/guests/register`,
        {
          name: formData.name,
          email: formData.email,
          table_number: parseInt(formData.table_number)
        }
      );
      
      navigate(`/menu/${data._id}`);
    } catch (err) {
      setError(err.response?.data?.detail || 'Une erreur s\'est produite');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen hero-section">
      <div className="hero-overlay min-h-screen flex flex-col items-center justify-center px-6 py-12">
        <div className="w-full max-w-md">
          <button
            onClick={() => navigate('/')}
            className="flex items-center gap-2 text-[#D4AF37] hover:text-[#F3E5AB] mb-8 transition-colors"
            data-testid="back-button"
          >
            <ArrowLeft size={20} />
            Retour
          </button>

          <div className="glass-surface rounded-2xl p-8 space-y-6">
            <div className="text-center space-y-2">
              <h2 className="text-3xl sm:text-4xl font-heading font-light text-[#D4AF37]" data-testid="registration-title">
                Inscription
              </h2>
              <p className="text-sm text-[#A3B8B0] verse-text">
                « Venez, car tout est prêt » - Luc 14:17
              </p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4" data-testid="guest-registration-form">
              <div>
                <label className="block text-sm font-medium text-white/90 mb-2">
                  Nom complet *
                </label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full bg-black/30 border border-[#D4AF37]/30 rounded-lg px-4 py-3 text-white placeholder-[#A3B8B0] focus:border-[#D4AF37] focus:outline-none transition-colors"
                  placeholder="Votre nom"
                  data-testid="name-input"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-white/90 mb-2">
                  Email (optionnel)
                </label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="w-full bg-black/30 border border-[#D4AF37]/30 rounded-lg px-4 py-3 text-white placeholder-[#A3B8B0] focus:border-[#D4AF37] focus:outline-none transition-colors"
                  placeholder="votre@email.com"
                  data-testid="email-input"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-white/90 mb-2">
                  Numéro de table *
                </label>
                <select
                  required
                  value={formData.table_number}
                  onChange={(e) => setFormData({ ...formData, table_number: e.target.value })}
                  className="w-full bg-black/30 border border-[#D4AF37]/30 rounded-lg px-4 py-3 text-white focus:border-[#D4AF37] focus:outline-none transition-colors"
                  data-testid="table-select"
                >
                  <option value="">Sélectionnez votre table</option>
                  {tables.map((table) => (
                    <option key={table.table_number} value={table.table_number}>
                      Table {table.table_number} ({table.places} places)
                    </option>
                  ))}
                </select>
              </div>

              {error && (
                <div className="bg-[#991B1B]/20 border border-[#991B1B] rounded-lg p-3 text-sm text-white" data-testid="error-message">
                  {error}
                </div>
              )}

              <button
                type="submit"
                disabled={loading}
                className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
                data-testid="submit-registration-button"
              >
                {loading ? 'Inscription...' : 'Continuer vers le menu'}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GuestRegistrationPage;
