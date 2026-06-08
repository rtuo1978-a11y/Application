import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import axios from 'axios';
import { LogOut, Plus, Table as TableIcon, Utensils, Eye, X } from 'lucide-react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '../components/ui/accordion';

const AdminDashboard = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [activeTab, setActiveTab] = useState('tables');
  
  const [tables, setTables] = useState([]);
  const [menu, setMenu] = useState([]);
  const [results, setResults] = useState([]);
  
  const [tableForm, setTableForm] = useState({ table_number: '', places: 1 });
  const [dishForm, setDishForm] = useState({ name: '', description: '' });
  
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [tablesRes, menuRes] = await Promise.all([
        axios.get(`${process.env.REACT_APP_BACKEND_URL}/api/tables`),
        axios.get(`${process.env.REACT_APP_BACKEND_URL}/api/menu`)
      ]);
      setTables(tablesRes.data);
      setMenu(menuRes.data);
    } catch (err) {
      console.error('Error fetching data:', err);
    }
  };

  const fetchResults = async () => {
    try {
      const { data } = await axios.get(
        `${process.env.REACT_APP_BACKEND_URL}/api/admin/results`,
        { withCredentials: true }
      );
      setResults(data);
    } catch (err) {
      setError('Impossible de charger les résultats');
    }
  };

  const handleCreateTable = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      await axios.post(
        `${process.env.REACT_APP_BACKEND_URL}/api/tables/create`,
        {
          table_number: parseInt(tableForm.table_number),
          places: parseInt(tableForm.places)
        },
        { withCredentials: true }
      );
      setSuccess('Table créée avec succès');
      setTableForm({ table_number: '', places: 1 });
      fetchData();
    } catch (err) {
      setError(err.response?.data?.detail || 'Erreur lors de la création');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateDish = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      await axios.post(
        `${process.env.REACT_APP_BACKEND_URL}/api/menu/create`,
        dishForm,
        { withCredentials: true }
      );
      setSuccess('Plat ajouté avec succès');
      setDishForm({ name: '', description: '' });
      fetchData();
    } catch (err) {
      setError(err.response?.data?.detail || 'Erreur lors de la création');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    await logout();
    navigate('/admin/login');
  };

  return (
    <div className="min-h-screen bg-[#0F2F20] py-8 px-6">
      <div className="max-w-7xl mx-auto space-y-8">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h1 className="text-3xl sm:text-4xl font-heading font-light text-[#D4AF37] tracking-tight" data-testid="admin-dashboard-title">
              Tableau de bord Admin
            </h1>
            <p className="text-sm text-[#A3B8B0] mt-2">Bienvenue, {user?.name}</p>
          </div>
          <button
            onClick={handleLogout}
            className="btn-secondary flex items-center gap-2"
            data-testid="logout-button"
          >
            <LogOut size={18} />
            Déconnexion
          </button>
        </div>

        {error && (
          <div className="bg-[#991B1B]/20 border border-[#991B1B] rounded-lg p-4 text-white flex justify-between items-center" data-testid="dashboard-error">
            <span>{error}</span>
            <button onClick={() => setError('')}><X size={18} /></button>
          </div>
        )}

        {success && (
          <div className="bg-green-900/20 border border-green-600 rounded-lg p-4 text-white flex justify-between items-center" data-testid="dashboard-success">
            <span>{success}</span>
            <button onClick={() => setSuccess('')}><X size={18} /></button>
          </div>
        )}

        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-3 bg-black/40 border border-[#D4AF37]/30 p-1 rounded-lg" data-testid="admin-tabs">
            <TabsTrigger 
              value="tables" 
              className="data-[state=active]:bg-[#D4AF37] data-[state=active]:text-black text-white rounded-md transition-all"
              data-testid="tables-tab"
            >
              <TableIcon size={18} className="mr-2" />
              Tables
            </TabsTrigger>
            <TabsTrigger 
              value="menu"
              className="data-[state=active]:bg-[#D4AF37] data-[state=active]:text-black text-white rounded-md transition-all"
              data-testid="menu-tab"
            >
              <Utensils size={18} className="mr-2" />
              Menu
            </TabsTrigger>
            <TabsTrigger 
              value="results"
              className="data-[state=active]:bg-[#D4AF37] data-[state=active]:text-black text-white rounded-md transition-all"
              data-testid="results-tab"
              onClick={fetchResults}
            >
              <Eye size={18} className="mr-2" />
              Résultats
            </TabsTrigger>
          </TabsList>

          <TabsContent value="tables" className="mt-6 space-y-6">
            <div className="glass-surface rounded-2xl p-6 space-y-4">
              <h2 className="text-2xl font-heading text-[#D4AF37] flex items-center gap-2">
                <Plus size={24} />
                Créer une nouvelle table
              </h2>
              <form onSubmit={handleCreateTable} className="space-y-4" data-testid="create-table-form">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-white/90 mb-2">
                      Numéro de table *
                    </label>
                    <input
                      type="number"
                      required
                      min="1"
                      value={tableForm.table_number}
                      onChange={(e) => setTableForm({ ...tableForm, table_number: e.target.value })}
                      className="w-full bg-black/30 border border-[#D4AF37]/30 rounded-lg px-4 py-3 text-white focus:border-[#D4AF37] focus:outline-none transition-colors"
                      placeholder="Ex: 1"
                      data-testid="table-number-input"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-white/90 mb-2">
                      Nombre de places *
                    </label>
                    <input
                      type="number"
                      required
                      min="1"
                      value={tableForm.places}
                      onChange={(e) => setTableForm({ ...tableForm, places: e.target.value })}
                      className="w-full bg-black/30 border border-[#D4AF37]/30 rounded-lg px-4 py-3 text-white focus:border-[#D4AF37] focus:outline-none transition-colors"
                      placeholder="Ex: 8"
                      data-testid="table-places-input"
                    />
                  </div>
                </div>
                <button
                  type="submit"
                  disabled={loading}
                  className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                  data-testid="create-table-button"
                >
                  {loading ? 'Création...' : 'Créer la table'}
                </button>
              </form>
            </div>

            <div className="glass-surface rounded-2xl p-6 space-y-4">
              <h2 className="text-2xl font-heading text-[#D4AF37]">Tables existantes</h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4" data-testid="tables-list">
                {tables.map((table, index) => (
                  <div
                    key={index}
                    className="bg-black/30 border border-[#D4AF37]/30 rounded-lg p-4 space-y-2"
                    data-testid={`table-item-${index}`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-2xl font-heading text-[#D4AF37]">Table {table.table_number}</span>
                      <TableIcon className="text-[#A3B8B0]" size={24} />
                    </div>
                    <p className="text-sm text-[#A3B8B0]">{table.places} place(s)</p>
                  </div>
                ))}
              </div>
            </div>
          </TabsContent>

          <TabsContent value="menu" className="mt-6 space-y-6">
            <div className="glass-surface rounded-2xl p-6 space-y-4">
              <h2 className="text-2xl font-heading text-[#D4AF37] flex items-center gap-2">
                <Plus size={24} />
                Ajouter un plat au menu
              </h2>
              <form onSubmit={handleCreateDish} className="space-y-4" data-testid="create-dish-form">
                <div>
                  <label className="block text-sm font-medium text-white/90 mb-2">
                    Nom du plat *
                  </label>
                  <input
                    type="text"
                    required
                    value={dishForm.name}
                    onChange={(e) => setDishForm({ ...dishForm, name: e.target.value })}
                    className="w-full bg-black/30 border border-[#D4AF37]/30 rounded-lg px-4 py-3 text-white focus:border-[#D4AF37] focus:outline-none transition-colors"
                    placeholder="Ex: Agneau rôti aux herbes"
                    data-testid="dish-name-input"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-white/90 mb-2">
                    Description (optionnel)
                  </label>
                  <textarea
                    value={dishForm.description}
                    onChange={(e) => setDishForm({ ...dishForm, description: e.target.value })}
                    rows="3"
                    className="w-full bg-black/30 border border-[#D4AF37]/30 rounded-lg px-4 py-3 text-white focus:border-[#D4AF37] focus:outline-none transition-colors resize-none"
                    placeholder="Description du plat..."
                    data-testid="dish-description-input"
                  />
                </div>
                <button
                  type="submit"
                  disabled={loading}
                  className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                  data-testid="create-dish-button"
                >
                  {loading ? 'Ajout...' : 'Ajouter le plat'}
                </button>
              </form>
            </div>

            <div className="glass-surface rounded-2xl p-6 space-y-4">
              <h2 className="text-2xl font-heading text-[#D4AF37]">Menu actuel</h2>
              <div className="space-y-3" data-testid="menu-list">
                {menu.map((dish, index) => (
                  <div
                    key={index}
                    className="bg-black/30 border border-[#D4AF37]/30 rounded-lg p-4 space-y-2"
                    data-testid={`menu-item-${index}`}
                  >
                    <div className="flex items-center gap-2">
                      <Utensils className="text-[#D4AF37]" size={20} />
                      <h3 className="text-lg font-semibold text-white">{dish.name}</h3>
                    </div>
                    {dish.description && (
                      <p className="text-sm text-[#A3B8B0] pl-7">{dish.description}</p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </TabsContent>

          <TabsContent value="results" className="mt-6">
            <div className="glass-surface rounded-2xl p-6 space-y-4">
              <h2 className="text-2xl font-heading text-[#D4AF37]">
                Vue d'ensemble des commandes
              </h2>
              <p className="text-sm text-[#A3B8B0] verse-text">
                « Celui qui a commencé en vous une bonne œuvre la mènera à son accomplissement » - Philippiens 1:6
              </p>

              <Accordion type="single" collapsible className="space-y-3" data-testid="admin-results-panel">
                {results.map((table, index) => (
                  <AccordionItem
                    key={index}
                    value={`table-${index}`}
                    className="bg-black/30 border border-[#D4AF37]/30 rounded-lg overflow-hidden"
                    data-testid={`result-table-${index}`}
                  >
                    <AccordionTrigger className="px-6 py-4 hover:bg-black/40 transition-colors text-left">
                      <div className="flex items-center justify-between w-full pr-4">
                        <span className="text-lg font-heading text-[#D4AF37]">
                          Table {table.table_number}
                        </span>
                        <span className="text-sm text-[#A3B8B0]">
                          {table.orders.length} commande(s)
                        </span>
                      </div>
                    </AccordionTrigger>
                    <AccordionContent className="px-6 pb-4">
                      {table.orders.length === 0 ? (
                        <p className="text-sm text-[#A3B8B0] italic">Aucune commande pour cette table</p>
                      ) : (
                        <div className="space-y-2">
                          {table.orders.map((order, orderIndex) => (
                            <div
                              key={orderIndex}
                              className="flex items-start gap-3 text-sm bg-black/20 rounded-lg p-3"
                              data-testid={`order-${index}-${orderIndex}`}
                            >
                              <span className="text-[#D4AF37] font-semibold">{orderIndex + 1}.</span>
                              <div>
                                <p className="text-white font-medium">{order.guest_name}</p>
                                <p className="text-[#A3B8B0]">{order.dish_name}</p>
                              </div>
                            </div>
                          ))}
                        </div>
                      )}
                    </AccordionContent>
                  </AccordionItem>
                ))}
              </Accordion>

              {results.length === 0 && (
                <p className="text-center text-[#A3B8B0] py-8">Aucune donnée disponible</p>
              )}
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default AdminDashboard;
