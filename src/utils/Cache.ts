const DEFULAT_TTL = 60 * 60 * 24; // 24 hours

const writeToCache = (url: string, data: any, ttl_sec?: number): void => {
  const ttl_millisec = ttl_sec ? ttl_sec * 1000 : DEFULAT_TTL * 1000;
  const item = {
    value: data,
    expiry: Date.now() + ttl_millisec,
  };
  localStorage.setItem(url, JSON.stringify(item));
};

const readFromCache = (url: string): any => {
  const res = localStorage.getItem(url);
  if (res === null) {
    return null;
  } else {
    const item = JSON.parse(res);
    const now = new Date();
    if (now.getTime() > item.expiry) {
      localStorage.removeItem(url);
      return null;
    } else {
      return item.value;
    }
  }
};

export { readFromCache, writeToCache };
