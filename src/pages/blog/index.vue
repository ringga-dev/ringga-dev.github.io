<template>
  <BlogListing :page="1" />
</template>

<script setup>
// Halaman 1 dari listing blog. Halaman 2+ dilayani /blog/page/[page].
// Semua logika listing (filter, sort, slice, pagination) ada di
// BlogListing.vue supaya hasil render halaman 1 dan /page/N identik.
</script>
