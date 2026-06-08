import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { ArrowLeft } from 'lucide-react';

const GalleryPage = () => {
  const navigate = useNavigate();
  const [gallery, setGallery] = useState([]);

  useEffect(() => {
    fetchGallery();
  }, []);

  const fetchGallery = async () => {
    try {
      const { data } = await axios.get(`${process.env.REACT_APP_BACKEND_URL}/api/gallery`);
      setGallery(data);
    } catch (err) {
      console.error('Error fetching gallery:', err);
    }
  };

  return (
    <div className="min-h-screen bg-[#0F2F20] py-12 px-6">
      <div className="max-w-7xl mx-auto space-y-12">
        <div className="flex items-center justify-between">
          <button
            onClick={() => navigate('/')}
            className="flex items-center gap-2 text-[#D4AF37] hover:text-[#F3E5AB] transition-colors"
            data-testid="back-from-gallery-button"
          >
            <ArrowLeft size={20} />
            Retour
          </button>
        </div>

        <div className="text-center space-y-4">
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-heading font-light text-[#D4AF37] tracking-tight" data-testid="gallery-title">
            Galerie Sacrée
          </h1>
          <p className="text-lg text-[#A3B8B0] verse-text max-w-2xl mx-auto">
            « La gloire de Dieu illumine le ciel et ses œuvres proclament sa grandeur »
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8" data-testid="gallery-grid">
          {gallery.map((item, index) => (
            <div
              key={index}
              className="gallery-item glass-surface rounded-2xl overflow-hidden"
              data-testid={`gallery-item-${index}`}
            >
              <div className="aspect-[4/3] overflow-hidden">
                <img
                  src={item.url}
                  alt={item.description}
                  className="w-full h-full object-cover"
                  loading="lazy"
                />
              </div>
              <div className="p-6 space-y-3">
                <h3 className="text-xl font-heading text-[#D4AF37]">{item.description}</h3>
                <p className="text-sm text-[#A3B8B0] verse-text italic">{item.verse}</p>
              </div>
            </div>
          ))}
        </div>

        <div className="glass-surface rounded-2xl p-8 text-center space-y-4">
          <h3 className="text-2xl font-heading text-[#D4AF37]">Méditation</h3>
          <p className="text-[#A3B8B0] verse-text max-w-3xl mx-auto">
            « Bienheureux ceux qui ont faim et soif de justice, car ils seront rassasiés. Bienheureux les cœurs purs, car ils verront Dieu. » - Matthieu 5:6-8
          </p>
        </div>
      </div>
    </div>
  );
};

export default GalleryPage;
