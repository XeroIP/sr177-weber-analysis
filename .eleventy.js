const refs = require("./src/_data/references.json");
const refMap = new Map(refs.map((r, i) => [r.id, i + 1]));

module.exports = function(eleventyConfig) {
  eleventyConfig.addPassthroughCopy("src/shared.css");
  eleventyConfig.addPassthroughCopy({ "src/assets": "assets" });
  eleventyConfig.addPassthroughCopy("src/robots.txt");

  eleventyConfig.addShortcode("cite", (id) => {
    const n = refMap.get(id);
    if (!n) throw new Error(`Unknown citation id: "${id}"`);
    return `<sup class="cite"><a href="/references.html#ref-${id}" aria-label="Reference ${n}">[${n}]</a></sup>`;
  });

  eleventyConfig.addShortcode("refCount", () => String(refs.length));

  eleventyConfig.addFilter("groupBy", (arr, key) =>
    arr.reduce((acc, item) => { (acc[item[key]] ||= []).push(item); return acc; }, {})
  );

  eleventyConfig.addFilter("refIndex", (id) => refMap.get(id) || "?");

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      data: "_data"
    },
    htmlTemplateEngine: "njk",
    markdownTemplateEngine: "njk"
  };
};
