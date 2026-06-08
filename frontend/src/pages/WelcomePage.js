import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Book } from 'lucide-react';

const WelcomePage = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen hero-section">
      <div className="hero-overlay min-h-screen flex flex-col">
        <div className="flex-1 flex flex-col items-center justify-center px-6 py-12">
          <div className="max-w-4xl mx-auto text-center space-y-8">
            <h1 className="text-5xl sm:text-6xl lg:text-7xl font-heading font-light text-[#D4AF37] tracking-tight" data-testid="main-title">
              Apotheosis ACE
            </h1>
            
            <p className="text-xl sm:text-2xl text-[#A3B8B0] verse-text font-light max-w-2xl mx-auto">
              « Je suis le pain de vie. Celui qui vient à moi n'aura jamais faim. »
            </p>
            
            <p className="text-base sm:text-lg text-white/80 max-w-xl mx-auto">
              Bienvenue à notre banquet sacré. Inscrivez-vous pour partager ce moment de grâce et de communion.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-6">
              <button
                onClick={() => navigate('/register')}
                className="btn-primary w-full sm:w-auto"
                data-testid="register-button"
              >
                S'inscrire au Banquet
              </button>
              
              <button
                onClick={() => navigate('/gallery')}
                className="btn-secondary w-full sm:w-auto flex items-center justify-center gap-2"
                data-testid="gallery-button"
              >
                <Book size={20} />
                Galerie Sacrée
              </button>
            </div>
          </div>
        </div>

        <footer className="py-6 text-center text-[#A3B8B0] text-sm">
          <p className="verse-text">« Heureux les invités au festin des noces de l'Agneau » - Apocalypse 19:9</p>
        </footer>
      </div>
    </div>
  );
};

export default WelcomePage;
