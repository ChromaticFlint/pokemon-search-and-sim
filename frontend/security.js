// Frontend security utilities and input validation

/**
 * Input sanitization and validation utilities
 */
export class InputValidator {
  // Constants
  static MAX_POKEMON_NAME_LENGTH = 50;
  static MAX_STATS_VALUES = 6;
  static MIN_STAT_VALUE = 0;
  static MAX_STAT_VALUE = 999;
  static MAX_LIMIT_VALUE = 1000;

  // Pokemon name pattern (letters, numbers, spaces, hyphens, apostrophes)
  static POKEMON_NAME_PATTERN = /^[a-zA-Z0-9\s\-'\.]+$/;

  /**
   * Validate Pokemon name input
   * @param {string} name - Pokemon name to validate
   * @returns {string} - Sanitized name
   * @throws {Error} - If validation fails
   */
  static validatePokemonName(name) {
    if (!name || typeof name !== 'string') {
      throw new Error('Pokemon name is required and must be a string');
    }

    // Strip whitespace
    name = name.trim();

    if (name.length === 0) {
      throw new Error('Pokemon name cannot be empty');
    }

    if (name.length > this.MAX_POKEMON_NAME_LENGTH) {
      throw new Error(`Pokemon name too long (max ${this.MAX_POKEMON_NAME_LENGTH} characters)`);
    }

    // Check for valid characters
    if (!this.POKEMON_NAME_PATTERN.test(name)) {
      throw new Error('Pokemon name contains invalid characters. Only letters, numbers, spaces, hyphens, and apostrophes are allowed');
    }

    return name;
  }

  /**
   * Validate stats string input
   * @param {string} statsStr - Stats string to validate
   * @returns {string} - Sanitized stats string
   * @throws {Error} - If validation fails
   */
  static validateStatsString(statsStr) {
    if (!statsStr || typeof statsStr !== 'string') {
      throw new Error('Stats string is required');
    }

    // Remove whitespace
    statsStr = statsStr.trim();

    if (!statsStr) {
      throw new Error('Stats string cannot be empty');
    }

    // Split by comma and validate
    const parts = statsStr.split(',');

    if (parts.length !== this.MAX_STATS_VALUES) {
      throw new Error(`Stats must contain exactly ${this.MAX_STATS_VALUES} values (HP,Attack,Defense,Special Attack,Special Defense,Speed)`);
    }

    const stats = [];
    for (let i = 0; i < parts.length; i++) {
      const part = parts[i].trim();

      // Check if it's a valid integer
      if (!/^-?\d+$/.test(part)) {
        throw new Error(`Stat value '${part}' is not a valid integer`);
      }

      const statValue = parseInt(part, 10);

      // Validate range
      if (statValue < this.MIN_STAT_VALUE || statValue > this.MAX_STAT_VALUE) {
        throw new Error(`Stat value ${statValue} is out of valid range (${this.MIN_STAT_VALUE}-${this.MAX_STAT_VALUE})`);
      }

      stats.push(statValue);
    }

    return stats.join(',');
  }

  /**
   * Validate limit parameter
   * @param {number|string} limit - Limit to validate
   * @returns {number} - Validated limit
   * @throws {Error} - If validation fails
   */
  static validateLimit(limit) {
    const numLimit = typeof limit === 'string' ? parseInt(limit, 10) : limit;

    if (isNaN(numLimit) || !Number.isInteger(numLimit)) {
      throw new Error('Limit must be a valid integer');
    }

    if (numLimit < 1) {
      throw new Error('Limit must be at least 1');
    }

    if (numLimit > this.MAX_LIMIT_VALUE) {
      throw new Error(`Limit too large (max ${this.MAX_LIMIT_VALUE})`);
    }

    return numLimit;
  }
}

/**
 * XSS protection utilities
 */
export class XSSProtection {
  /**
   * Escape HTML characters to prevent XSS
   * @param {string} text - Text to escape
   * @returns {string} - Escaped text
   */
  static escapeHtml(text) {
    if (typeof text !== 'string') {
      return text;
    }

    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  /**
   * Sanitize URL to prevent XSS
   * @param {string} url - URL to sanitize
   * @returns {string} - Sanitized URL
   */
  static sanitizeUrl(url) {
    if (typeof url !== 'string') {
      return '';
    }

    // Only allow http, https, and data URLs
    const allowedProtocols = /^(https?:|data:)/i;
    
    if (!allowedProtocols.test(url)) {
      return '';
    }

    // Remove javascript: and other dangerous protocols
    const dangerousProtocols = /^(javascript:|vbscript:|data:text\/html)/i;
    
    if (dangerousProtocols.test(url)) {
      return '';
    }

    return url;
  }
}

/**
 * API security utilities
 */
export class APISecurityUtils {
  /**
   * Add security headers to fetch requests
   * @param {RequestInit} options - Fetch options
   * @returns {RequestInit} - Options with security headers
   */
  static addSecurityHeaders(options = {}) {
    return {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        ...options.headers
      }
    };
  }

  /**
   * Validate API response
   * @param {Response} response - Fetch response
   * @throws {Error} - If response is invalid
   */
  static validateResponse(response) {
    if (!response.ok) {
      if (response.status === 429) {
        throw new Error('Too many requests. Please try again later.');
      } else if (response.status === 400) {
        throw new Error('Invalid input. Please check your data and try again.');
      } else if (response.status === 404) {
        throw new Error('Pokemon not found.');
      } else if (response.status >= 500) {
        throw new Error('Server error. Please try again later.');
      } else {
        throw new Error(`Request failed with status ${response.status}`);
      }
    }
  }

  /**
   * Sanitize API response data
   * @param {any} data - Response data
   * @returns {any} - Sanitized data
   */
  static sanitizeResponseData(data) {
    if (typeof data === 'string') {
      return XSSProtection.escapeHtml(data);
    }

    if (Array.isArray(data)) {
      return data.map(item => this.sanitizeResponseData(item));
    }

    if (data && typeof data === 'object') {
      const sanitized = {};
      for (const [key, value] of Object.entries(data)) {
        sanitized[key] = this.sanitizeResponseData(value);
      }
      return sanitized;
    }

    return data;
  }
}

/**
 * Rate limiting for client-side
 */
export class ClientRateLimit {
  constructor() {
    this.requests = new Map();
    this.maxRequestsPerMinute = 30; // Conservative client-side limit
  }

  /**
   * Check if request should be rate limited
   * @param {string} endpoint - API endpoint
   * @returns {boolean} - True if rate limited
   */
  isRateLimited(endpoint) {
    const now = Date.now();
    const windowStart = now - 60000; // 1 minute window

    if (!this.requests.has(endpoint)) {
      this.requests.set(endpoint, []);
    }

    const endpointRequests = this.requests.get(endpoint);
    
    // Remove old requests
    const recentRequests = endpointRequests.filter(time => time > windowStart);
    this.requests.set(endpoint, recentRequests);

    // Check if over limit
    if (recentRequests.length >= this.maxRequestsPerMinute) {
      return true;
    }

    // Add current request
    recentRequests.push(now);
    return false;
  }
}

// Global rate limiter instance
export const clientRateLimit = new ClientRateLimit();
