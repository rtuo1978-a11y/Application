import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { ArrowLeft } from 'lucide-react';

const AdminLoginPage = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const result = await login(formData.email, formData.password);
    
    if (result.success) {
      navigate('/admin/dashboard');
    } else {
      setError(result.error);
    }
    
    setLoading(false);
  };

  return (
    <div className="min-h-screen hero-section">
      <div className="hero-overlay min-h-screen flex flex-col items-center justify-center px-6 py-12">
        <div className="w-full max-w-md">
          <button
            onClick={() => navigate('/')}
            className="flex items-center gap-2 text-[#D4AF37] hover:text-[#F3E5AB] mb-8 transition-colors"
            data-testid="admin-back-button"
          >
            <ArrowLeft size={20} />
            Retour
          </button>

          <div className="glass-surface rounded-2xl p-8 space-y-6">
            <div className="text-center space-y-2">
              <h2 className="text-3xl sm:text-4xl font-heading font-light text-[#D4AF37]" data-testid="admin-login-title">
                Connexion Admin
              </h2>
              <p className="text-sm text-[#A3B8B0] verse-text">
                « Tu es le berger du troupeau »
              </p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4" data-testid="admin-login-form">
              <div>
                <label className="block text-sm font-medium text-white/90 mb-2">
                  Email
                </label>
                <input
                  type="email"
                  required
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="w-full bg-black/30 border border-[#D4AF37]/30 rounded-lg px-4 py-3 text-white placeholder-[#A3B8B0] focus:border-[#D4AF37] focus:outline-none transition-colors"
                  placeholder="admin@apotheosis.com"
                  data-testid="admin-email-input"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-white/90 mb-2">
                  Mot de passe
                </label>
                <input
                  type="password"
                  required
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  className="w-full bg-black/30 border border-[#D4AF37]/30 rounded-lg px-4 py-3 text-white placeholder-[#A3B8B0] focus:border-[#D4AF37] focus:outline-none transition-colors"
                  placeholder="••••••••"
                  data-testid="admin-password-input"
                />
              </div>

              {error && (
                <div className="bg-[#991B1B]/20 border border-[#991B1B] rounded-lg p-3 text-sm text-white" data-testid="admin-error-message">
                  {error}
                </div>
              )}

              <button
                type="submit"
                disabled={loading}
                className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
                data-testid="admin-login-button"
              >
                {loading ? 'Connexion...' : 'Se connecter'}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminLoginPage;
