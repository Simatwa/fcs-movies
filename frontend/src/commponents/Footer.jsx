const Footer = () => {
	return (
		<footer className='py-6 md:px-8 md:py-0 bg-black text-white border-t border-gray-800'>
			<div className='flex flex-col items-center justify-between gap-4 md:h-24 md:flex-row'>
				<p className='text-center text-sm leading-loose text-muted-foreground md:text-left'>
					Our services are available <strong>24/7</strong>, easy to download, and cost-effective to maintain. 
					<br /> © {new Date().getFullYear()} Fcs movies. All rights reserved.
				</p>
			</div>
		</footer>
	);
};
export default Footer;
