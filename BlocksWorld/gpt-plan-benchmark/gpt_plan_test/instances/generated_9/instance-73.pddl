

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(ontable b)
(on c g)
(on d i)
(ontable e)
(on f b)
(on g e)
(on h c)
(ontable i)
(clear a)
(clear d)
(clear f)
(clear h)
)
(:goal
(and
(on b f)
(on c d)
(on e g)
(on g h)
(on h i))
)
)


