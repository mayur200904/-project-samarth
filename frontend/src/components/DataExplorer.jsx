import { useState, useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import { HardDrive, RefreshCw, Search, ExternalLink, Loader2 } from 'lucide-react'
import { getDatasets, refreshDataset } from '../services/api'

function DataExplorer() {
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [searchTerm, setSearchTerm] = useState('')
  const [refreshingId, setRefreshingId] = useState(null)

  const { data: datasets, isLoading, refetch } = useQuery({
    queryKey: ['datasets'],
    queryFn: getDatasets
  })

  const filteredDatasets = datasets?.filter(ds => {
    const matchesCategory = selectedCategory === 'all' || ds.category === selectedCategory
    const matchesSearch = ds.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         ds.description.toLowerCase().includes(searchTerm.toLowerCase())
    return matchesCategory && matchesSearch
  })

  const handleRefresh = async (datasetId) => {
    setRefreshingId(datasetId)
    try {
      await refreshDataset(datasetId)
      await refetch()
    } catch (error) {
      console.error('Refresh failed:', error)
    } finally {
      setRefreshingId(null)
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="card p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Available Datasets</h2>
            <p className="text-gray-600 mt-1">
              Explore agricultural and climate data from data.gov.in
            </p>
          </div>
          <div className="flex items-center space-x-2 text-sm text-gray-600">
            <HardDrive className="w-5 h-5" />
            <span>{filteredDatasets?.length || 0} datasets</span>
          </div>
        </div>

        {/* Filters */}
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search datasets..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              />
            </div>
          </div>
          
          <div className="flex space-x-2">
            <button
              onClick={() => setSelectedCategory('all')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                selectedCategory === 'all'
                  ? 'bg-green-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              All
            </button>
            <button
              onClick={() => setSelectedCategory('agriculture')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                selectedCategory === 'agriculture'
                  ? 'bg-green-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Agriculture
            </button>
            <button
              onClick={() => setSelectedCategory('climate')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                selectedCategory === 'climate'
                  ? 'bg-green-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Climate
            </button>
          </div>
        </div>
      </div>

      {/* Datasets Grid */}
      {isLoading ? (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="w-8 h-8 text-green-600 animate-spin" />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredDatasets?.map((dataset) => (
            <div key={dataset.dataset_id} className="card p-6 hover:shadow-xl transition-shadow">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center space-x-2">
                  <div className={`w-3 h-3 rounded-full ${
                    dataset.category === 'agriculture' ? 'bg-green-500' : 'bg-blue-500'
                  }`}></div>
                  <span className="text-xs font-semibold text-gray-500 uppercase">
                    {dataset.category}
                  </span>
                </div>
                <button
                  onClick={() => handleRefresh(dataset.dataset_id)}
                  disabled={refreshingId === dataset.dataset_id}
                  className="text-gray-400 hover:text-green-600 transition-colors"
                  title="Refresh dataset"
                >
                  <RefreshCw className={`w-4 h-4 ${
                    refreshingId === dataset.dataset_id ? 'animate-spin' : ''
                  }`} />
                </button>
              </div>

              <h3 className="text-lg font-bold text-gray-900 mb-2">
                {dataset.name}
              </h3>
              
              <p className="text-sm text-gray-600 mb-4 line-clamp-3">
                {dataset.description}
              </p>

              <div className="space-y-2 mb-4">
                <div className="flex items-center justify-between text-xs">
                  <span className="text-gray-500">Rows:</span>
                  <span className="font-semibold text-gray-700">
                    {dataset.row_count?.toLocaleString() || 'N/A'}
                  </span>
                </div>
                <div className="flex items-center justify-between text-xs">
                  <span className="text-gray-500">Columns:</span>
                  <span className="font-semibold text-gray-700">
                    {dataset.fields?.length || 0}
                  </span>
                </div>
                <div className="flex items-center justify-between text-xs">
                  <span className="text-gray-500">Last Updated:</span>
                  <span className="font-semibold text-gray-700">
                    {dataset.last_updated ? new Date(dataset.last_updated).toLocaleDateString() : 'N/A'}
                  </span>
                </div>
              </div>

              <div className="flex flex-wrap gap-1 mb-4">
                {dataset.fields?.slice(0, 5).map((field, idx) => (
                  <span
                    key={idx}
                    className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded"
                  >
                    {field}
                  </span>
                ))}
                {dataset.fields?.length > 5 && (
                  <span className="text-xs text-gray-500 px-2 py-1">
                    +{dataset.fields.length - 5} more
                  </span>
                )}
              </div>

              <a
                href={dataset.url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center justify-center space-x-2 w-full py-2 px-4 border border-green-600 text-green-600 rounded-lg hover:bg-green-50 transition-colors"
              >
                <span className="text-sm font-medium">View on data.gov.in</span>
                <ExternalLink className="w-4 h-4" />
              </a>
            </div>
          ))}
        </div>
      )}

      {filteredDatasets?.length === 0 && !isLoading && (
        <div className="text-center py-12">
          <HardDrive className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">No datasets found matching your criteria</p>
        </div>
      )}
    </div>
  )
}

export default DataExplorer
