const refs = require("./src/_data/references.json");
const refMap = new Map(refs.map((r, i) => [r.id, i + 1]));
const PATH_PREFIX = "/sr177-weber-analysis";

module.exports = function(eleventyConfig) {
  eleventyConfig.addPassthroughCopy("src/shared.css");
  eleventyConfig.addPassthroughCopy({ "src/assets": "assets" });
  eleventyConfig.addPassthroughCopy("src/robots.txt");

  eleventyConfig.addShortcode("cite", (id) => {
    const n = refMap.get(id);
    if (!n) throw new Error(`Unknown citation id: "${id}"`);
    return `<sup class="cite"><a href="${PATH_PREFIX}/references.html#ref-${id}" aria-label="Reference ${n}">[${n}]</a></sup>`;
  });

  eleventyConfig.addShortcode("refCount", () => String(refs.length));

  eleventyConfig.addFilter("groupBy", (arr, key) =>
    arr.reduce((acc, item) => { (acc[item[key]] ||= []).push(item); return acc; }, {})
  );

  eleventyConfig.addFilter("refIndex", (id) => refMap.get(id) || "?");

  eleventyConfig.addFilter("sortByDateDesc", (arr) =>
    [...arr].sort((a, b) => String(b.date).localeCompare(String(a.date)))
  );

  eleventyConfig.addFilter("flattenNav", (items) => {
    const flattened = [];
    const visit = (item) => {
      if (item.url) flattened.push(item);
      if (item.children) item.children.forEach(visit);
    };
    items.forEach(visit);
    return flattened;
  });

  eleventyConfig.addFilter("isNavActive", (item, navKey) => {
    if (item.key === navKey) return true;
    return Boolean(item.children?.some((child) => child.key === navKey));
  });

  eleventyConfig.addFilter("navPath", (items, navKey) => {
    const visit = (navItems, ancestors) => {
      for (const item of navItems) {
        const path = [...ancestors, item];
        if (item.key === navKey) return path;
        if (item.children) {
          const childPath = visit(item.children, path);
          if (childPath) return childPath;
        }
      }
      return null;
    };

    return visit(items, []) || [];
  });

  eleventyConfig.addFilter("navIndex", (items, navKey) =>
    items.findIndex((item) => item.key === navKey)
  );

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      data: "_data"
    },
    pathPrefix: PATH_PREFIX + "/",
    htmlTemplateEngine: "njk",
    markdownTemplateEngine: "njk"
  };
};
