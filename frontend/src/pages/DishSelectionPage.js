import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Clock, CheckCircle, ArrowLeft } from 'lucide-react';

const DishSelectionPage = () => {
  const { guestId } = useParams();
  const navigate = useNavigate();
  const [guest, setGuest] = useState(null);
  const [menu, setMenu] = useState([]);
  const [selectedDish, setSelectedDish] = useState('');
  const [orderId, setOrderId] = useState(null);
  const [timeRemaining, setTimeRemaining] = useState(null);
  const [isLocked, setIsLocked] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchGuestAndMenu();
  }, [guestId]);

  useEffect(() => {
    if (timeRemaining !== null && timeRemaining > 0 && !isLocked) {
      const timer = setInterval(() => {
        setTimeRemaining((prev) => {
          if (prev <= 1) {
            setIsLocked(true);
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
      return () => clearInterval(timer);
    }
  }, [timeRemaining, isLocked]);

  const fetchGuestAndMenu = async () => {
    try {
      const [guestRes, menuRes] = await Promise.all([
        axios.get(`${process.env.REACT_APP_BACKEND_URL}/api/guests/${guestId}`),
        axios.get(`${process.env.REACT_APP_BACKEND_URL}/api/menu`)
      ]);
      setGuest(guestRes.data);
      setMenu(menuRes.data);
    } catch (err) {
      setError('Impossible de charger les données');
    }
  };

  const handleDishSelect = async (dishName) => {
    if (isLocked) {
      setError('Votre sélection est verrouillée');
      return;
    }

    setError('');
    setLoading(true);

    try {
      if (orderId) {
        await axios.put(
          `${process.env.REACT_APP_BACKEND_URL}/api/orders/${orderId}/update`,
          { dish_name: dishName }
        );
        setSelectedDish(dishName);
        setSuccess('Plat modifié avec succès');
      } else {
        const { data } = await axios.post(
          `${process.env.REACT_APP_BACKEND_URL}/api/orders/create`,
          { guest_id: guestId, dish_name: dishName }
        );
        setOrderId(data._id);
        setSelectedDish(dishName);
        setTimeRemaining(120);
        setSuccess('Plat sélectionné avec succès. Vous avez 2 minutes pour modifier.');
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Une erreur s\'est produite');
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (!guest) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#0F2F20]">
        <div className="text-[#D4AF37] text-xl font-heading">Chargement...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen hero-section">
      <div className="hero-overlay min-h-screen py-12 px-6">
        <div className="max-w-4xl mx-auto space-y-8">
          <button
            onClick={() => navigate('/')}
            className="flex items-center gap-2 text-[#D4AF37] hover:text-[#F3E5AB] transition-colors"
            data-testid="back-to-home-button"
          >
            <ArrowLeft size={20} />
            Retour à l'accueil
          </button>

          <div className="glass-surface rounded-2xl p-8 space-y-6">
            <div className="text-center space-y-2">
              <h2 className="text-3xl sm:text-4xl font-heading font-light text-[#D4AF37]" data-testid="menu-title">
                Menu du Banquet
              </h2>
              <p className="text-sm text-[#A3B8B0]">
                Bienvenue {guest.name} - Table {guest.table_number}
              </p>
              <p className="text-xs text-[#A3B8B0] verse-text">
                « Goûtez et voyez combien l'Éternel est bon » - Psaume 34:9
              </p>
            </div>

            {timeRemaining !== null && !isLocked && (
              <div className="bg-[#D4AF37]/10 border border-[#D4AF37] rounded-lg p-4 flex items-center gap-3" data-testid="timer-display">
                <Clock className="text-[#D4AF37]" size={24} />
                <div>
                  <p className="text-white font-medium">Temps restant pour modifier</p>
                  <p className="text-2xl font-heading text-[#D4AF37] countdown-timer">
                    {formatTime(timeRemaining)}
                  </p>
                </div>
              </div>
            )}

            {isLocked && selectedDish && (
              <div className="bg-green-900/20 border border-green-600 rounded-lg p-4 flex items-center gap-3" data-testid="locked-message">
                <CheckCircle className="text-green-400" size={24} />
                <div>
                  <p className="text-white font-medium">Votre choix est confirmé</p>
                  <p className="text-sm text-[#A3B8B0]">Vous avez sélectionné: {selectedDish}</p>
                </div>
              </div>
            )}

            {error && (
              <div className="bg-[#991B1B]/20 border border-[#991B1B] rounded-lg p-3 text-sm text-white" data-testid="error-display">
                {error}
              </div>
            )}

            {success && (
              <div className="bg-green-900/20 border border-green-600 rounded-lg p-3 text-sm text-white" data-testid="success-message">
                {success}
              </div>
            )}

            <div className="space-y-4" data-testid="dish-selection-form">
              <h3 className="text-xl font-heading text-white">Choisissez votre plat</h3>
              <div className="grid gap-4">
                {menu.map((dish, index) => (
                  <button
                    key={index}
                    onClick={() => handleDishSelect(dish.name)}
                    disabled={isLocked || loading}
                    className={`text-left p-6 rounded-lg border-2 transition-all ${
                      selectedDish === dish.name
                        ? 'border-[#D4AF37] bg-[#D4AF37]/10'
                        : 'border-[#D4AF37]/30 bg-black/20 hover:border-[#D4AF37] hover:bg-black/40'
                    } disabled:opacity-50 disabled:cursor-not-allowed`}
                    data-testid={`dish-option-${index}`}
                  >
                    <h4 className="text-lg font-semibold text-[#D4AF37] mb-2">{dish.name}</h4>
                    {dish.description && (
                      <p className="text-sm text-[#A3B8B0]">{dish.description}</p>
                    )}
                    {selectedDish === dish.name && (
                      <div className="mt-3 flex items-center gap-2 text-sm text-white">
                        <CheckCircle size={16} className="text-[#D4AF37]" />
                        Sélectionné
                      </div>
                    )}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DishSelectionPage;
